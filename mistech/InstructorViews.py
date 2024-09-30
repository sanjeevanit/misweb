import csv
import logging

import face_recognition
import cv2
import json
import dlib
import numpy as np
import datetime
import asyncio
import os
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.core import serializers
from django.forms import formset_factory
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip
from mistech.face_recognition import recognize_student_face, load_known_face_encodings
from mistech.form import AddTermForm, AddLessonForm, EditLessonForm, EditTermForm
from mistech.models import Attendance, Course, Student, Staff, Subject, SessionYr, CustomUser, LeaveReportSf, \
    FeedbackSf, Batch, Task, Module, Lplan, StudentResult, NotificationSf
from django.contrib.auth.decorators import login_required
from channels.db import database_sync_to_async
from django.http import StreamingHttpResponse
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.lib import colors
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.utils import timezone
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageTemplate, Spacer, Flowable, Frame
from reportlab.lib.units import inch
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.platypus.frames import Frame

from django.shortcuts import render
from .models import Course, Subject, Student


def instructor_home(request):
    # For Fetch All Student Under Staff
    subjects = Subject.objects.filter(sf_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Course.objects.get(c_id=subject.c_id.c_id)  # Modify this line
        course_id_list.append(course.c_id)  # Modify this line

    final_course = list(set(course_id_list))  # Simplify deduplication
    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(sub_id__in=subjects).count()
    students_count = Student.objects.filter(c_id__in=final_course).count()

    # Fetch All Approve Leave
    staff = Staff.objects.get(admin=request.user.id)
    leave_count = LeaveReportSf.objects.filter(sf_id=staff.sf_id, lrs_status=1).count()
    subject_count = subjects.count()

    # Fetch Attendance Data by Subject
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(sub_id=subject.sub_id).count()
        subject_list.append(subject.sub_code)
        attendance_list.append(attendance_count1)

    students_attendance = Student.objects.filter(c_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = Attendance.objects.filter(status="Present", st_id=student.st_id).count()
        attendance_absent_count = Attendance.objects.filter(status="Absent", st_id=student.st_id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request, "instructor_templates/instructor_home_content.html",
                  {"students_count": students_count, "attendance_count": attendance_count, "leave_count": leave_count,
                   "subject_count": subject_count, "subject_list": subject_list, "attendance_list": attendance_list,
                   "student_list": student_list, "present_list": student_list_attendance_present,
                   "absent_list": student_list_attendance_absent})


def mark_absent_students(students, course, subject, batch, session_yr, staff):
    """
    Marks absent students after 2 minutes if their attendance status is not "Present".
    """
    for student in students:
        st_id = student.st_idNo
        # Check if the student's attendance has already been marked as "Present" within the last 2 minutes
        last_attendance = Attendance.objects.filter(
            st_id=student, c_id=course, b_id=batch, yr_id=session_yr,
            created_at__gte=timezone.now() - timezone.timedelta(minutes=2),
            status='Present'
        ).exists()

        if not last_attendance:
            # Mark the student as absent if their attendance status is not "Present"
            Attendance.objects.create(st_id=student, status='Absent', c_id=course, sub_id=subject, b_id=batch,
                                      yr_id=session_yr, sf_id=staff.admin)


def get_subject(request):
    c_name = request.GET.get('c_id')
    try:
        # Find the Course instance based on the provided course name
        course = Course.objects.get(c_name=c_name)
        # Retrieve subjects for the given course
        subjects = Subject.objects.filter(c_id=course).values('sub_id', 'sub_name')

        return JsonResponse({'subjects': list(subjects)})
    except Course.DoesNotExist:
        return JsonResponse({'subjects': []})


def get_batches(request):
    c_name = request.GET.get('c_id')
    try:
        # Find the Course instance based on the provided course name
        course = Course.objects.get(c_name=c_name)
        # Retrieve subjects for the given course
        batches = Batch.objects.filter(c_id=course).values('b_id', 'b_code')

        return JsonResponse({'batches': list(batches)})
    except Course.DoesNotExist:
        return JsonResponse({'batches': []})


logger = logging.getLogger(__name__)


@login_required
def instructor_take_attendance(request):
    if request.method == 'POST':
        sub_name = request.POST.get('sub_name')
        c_name = request.POST.get('c_name')
        b_code = request.POST.get('b_code')
        yr_id = request.POST.get('yr_id')

        try:
            course = Course.objects.get(c_name__iexact=c_name.strip())
            subjects = Subject.objects.filter(sub_name__iexact=sub_name.strip(), c_id=course)
            batches = Batch.objects.filter(b_code__iexact=b_code.strip(), c_id=course)

            if not (subjects.exists() and batches.exists()):
                return JsonResponse(
                    {'status': 'error', 'message': f'Subject or Batch not found for Course {c_name}'},
                    status=400)

            subject = subjects.first()
            batch = batches.first()
            staff = request.user.staff
            session_yr = get_object_or_404(SessionYr, yr_id=yr_id)
            students = Student.objects.filter(c_id=course, b_id=batch)

            known_encodings, known_ids = load_known_face_encodings(students)

            for student in students:
                profile_img_path = student.admin.profile_img.path
                if os.path.exists(profile_img_path):
                    known_image = face_recognition.load_image_file(profile_img_path)
                    known_encoding = face_recognition.face_encodings(known_image)[0]
                    known_encodings.append(known_encoding)
                    known_ids.append({'id': student.st_idNo, 'last_marked_time': None})
                else:
                    print(f"Profile image not found for student {student.st_idNo}")

            last_marked_times = {student_info['id']: None for student_info in known_ids}
            video_capture = cv2.VideoCapture(0)
            attendance_status = 'Absent'
            st_idNo = 'Please register to the system'  # Default value for st_idNo
            recognized_st_info = None
            start_time = datetime.now()

            while (datetime.now() - start_time).total_seconds() <= 120:  # Two minutes interval
                ret, frame = video_capture.read()
                if not ret:
                    break

                unknown_encoding = face_recognition.face_encodings(frame)
                if len(unknown_encoding) > 0:
                    match_index = recognize_student_face(known_encodings, unknown_encoding[0])
                    if match_index is not None:
                        student_info = known_ids[match_index]
                        last_marked_time = last_marked_times[student_info['id']]

                        if (last_marked_time is None or datetime.now() - last_marked_time > timedelta(seconds=120)):
                            existing_attendance = Attendance.objects.filter(
                                st_id=student, yr_id=session_yr, b_id=batch, c_id=course,
                                created_at__gte=timezone.now() - timezone.timedelta(minutes=2),
                                status='Present'
                            ).exists()

                            if not existing_attendance:
                                # Check if student is registered for the selected session year, batch code, and course name
                                if not Student.objects.filter(st_idNo=student_info['id'], yr_id=session_yr, b_id=batch,
                                                              c_id=course).exists():
                                    return JsonResponse({'status': 'warning',
                                                         'message': f'Student {student_info["id"]} is not registered for the specified session year, batch code, and course name.'})

                                attendance_status = 'Present'
                                st_idNo = student_info['id']
                                student_info['last_marked_time'] = datetime.now()
                                recognized_st_info = student_info
                                break
                            else:
                                attendance_status = 'Already Marked'
                                st_idNo = student_info['id']
                                recognized_st_info = student_info
                                break
                    else:
                        attendance_status = 'Unknown'
                        return JsonResponse({'status': 'error',
                                             'message': 'Student not found in the system. Please register to the system.'})

            video_capture.release()

            if st_idNo == 'Please register to the system':
                return JsonResponse(
                    {'status': 'error', 'message': 'Student not found in the system. Please register to the system.'})
            elif attendance_status == 'Already Marked':
                return JsonResponse({'status': 'error',
                                     'message': f'Student {st_idNo} attendance has already been taken within the last two minutes.'})
            elif attendance_status == 'Present':
                student = Student.objects.get(st_idNo=st_idNo)
                session_yr = SessionYr.object.get(yr_id=yr_id)

                Attendance.objects.create(st_id=student, status='Present', c_id=course, sub_id=subject, b_id=batch,
                                          yr_id=session_yr, sf_id=staff.admin)

                mark_absent_students(students, course, subject, batch, session_yr, staff)

                return JsonResponse(
                    {'status': 'success', 'message': f'Student {st_idNo} attendance marked as {attendance_status}.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Unable to recognize the student.'})

        except (Course.DoesNotExist, Subject.DoesNotExist, Batch.DoesNotExist, Student.DoesNotExist,
                SessionYr.DoesNotExist) as e:
            print("Error: ", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    else:
        staff = Staff.objects.all()
        subject = Subject.objects.all()
        batch = Batch.objects.all()
        course = Course.objects.all()
        session_yr = SessionYr.object.all()
        return render(request, 'instructor_templates/instructor_take_attendance.html',
                      {'staff': staff, 'subject': subject, 'batch': batch, 'course': course, 'session_yr': session_yr})


def instructor_apply_leave(request):
    current_date = datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        lrs_msg = request.POST.get("lrs_msg", "")
        print("Leave Reason:", lrs_msg)  # For debugging
    else:
        lrs_msg = ""  # Set default value if not provided

    instructor_obj = Staff.objects.get(admin=request.user.id)
    lv_data = LeaveReportSf.objects.filter(sf_id=instructor_obj)

    return render(request, "instructor_templates/instructor_apply_leave.html",
                  {"lv_data": lv_data, "lrs_msg": lrs_msg, "current_date": current_date})


def instructor_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("instructor_apply_leave"))
    else:
        lrs_date = request.POST.get("lrs_date")
        lrs_msg = request.POST.get("lrs_msg")  # Corrected variable name
        medical_img = request.FILES.get("medical_img")

        instructor_obj = Staff.objects.get(admin=request.user.id)
        try:
            lv_report = LeaveReportSf(sf_id=instructor_obj, lrs_date=lrs_date, lrs_msg=lrs_msg, lrs_status=0)
            if lrs_msg.lower() == "medical" and medical_img:
                lv_report.medical_img = medical_img
            lv_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("instructor_apply_leave"))
        except Exception as e:
            messages.error(request, f"Failed To Apply for Leave: {e}")
            return HttpResponseRedirect(reverse("instructor_apply_leave"))


@csrf_exempt
def mark_notification_as_readSF(request):
    notifications = NotificationSf.objects.filter(sf_id=request.user.id, is_read=False)
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return JsonResponse({'success': True})


def fetch_notificationsSF(request):
    notifications = NotificationSf.objects.filter(sf_id=request.user.id)[:5]  # Get latest 5 notifications
    notification_html = ""
    for notification in notifications:
        notification_html += f"<a class='dropdown-item' href='/feedback/{notification.pk}'>{notification.notify_sf}</a>"
    data = {
        'count': NotificationSf.objects.filter(sf_id=request.user.id, is_read=False).count(),
        # Count only unread notifications
        'html': notification_html,
    }
    return JsonResponse(data)


def instructor_feedback(request):
    instructor_obj = Staff.objects.get(admin=request.user.id)
    feedback_data = FeedbackSf.objects.filter(sf_id=instructor_obj)

    return render(request, "instructor_templates/instructor_feedback.html", {"feedback_data": feedback_data})


def instructor_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("instructor_feedback"))
    else:
        fbs_msg = request.POST.get("fbs_msg")

        instructor_obj = Staff.objects.get(admin=request.user.id)
        # try:
        feedback = FeedbackSf(sf_id=instructor_obj, fbs=fbs_msg, fbs_rpy="")
        feedback.save()

        notification = NotificationSf.objects.create(
            notify_sf=f"New feedback message from instructor: {instructor_obj}",
            sf_id=instructor_obj,
            created_at=timezone.now()
        )

        messages.success(request, "Successfully Sent Feedback")
        return HttpResponseRedirect(reverse("instructor_feedback"))
        # except:
        #     messages.error(request, "Failed To Send Feedback")
        #     return HttpResponseRedirect(reverse("instructor_feedback"))


def instructor_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "instructor_templates/instructor_profile.html", {"user": user})


def instructor_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("instructor_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("instructor_profile"))
        except:
            messages.error(request, "Failed to Updated Profile")
            return HttpResponseRedirect(reverse("instructor_profile"))


@csrf_exempt
def check_taskname_exist(request):
    tk_name = request.POST.get("tk_name", "").strip()  # Remove leading/trailing whitespaces
    if tk_name:
        # Check if a similar trade name exists (case-insensitive and ignoring spaces)
        task_exists = Task.objects.filter(
            Q(tk_name__icontains=tk_name) | Q(tk_name__icontains=tk_name.replace(" ", ""))
        ).exists()
        return JsonResponse({'exists': task_exists})  # Return the result as JSON
    else:
        return JsonResponse({'exists': False})


def instructor_task(request):
    form = AddTermForm()
    return render(request, "instructor_templates/instructor_term_note.html", {"form": form})


def instructor_task_save(request):
    if request.method == "POST":
        form = AddTermForm(request.POST)
        if form.is_valid():
            tk_name = form.cleaned_data["tk_name"]
            tk_date = form.cleaned_data["tk_date"]
            tk_wk = form.cleaned_data["tk_wk"]
            status = form.cleaned_data["status"]
            mod_id = form.cleaned_data["module"]
            sf_id = request.user  # Assuming  have a way to access the logged-in user

            try:
                task = Task(tk_name=tk_name, tk_date=tk_date, tk_wk=tk_wk, status=status, sf_id=sf_id)
                module_object = Module.objects.get(mod_id=mod_id)
                task.mod_id = module_object
                task.save()
                messages.success(request, "Task successfully added")
                return HttpResponseRedirect(reverse("instructor_task"))
            except Exception as e:
                print(e)
                messages.error(request, "Failed to add task")
        else:
            messages.error(request, "Form is not valid")
    else:
        form = AddTermForm()

    return render(request, "instructor_templates/instructor_term_note.html", {"form": form})


def manage_instructor_task(request):
    search_query = request.GET.get('search', '')
    user = request.user
    tasks = Task.objects.filter(sf_id=user).order_by('tk_id')

    if search_query:
        tasks = tasks.filter(
            Q(tk_name__icontains=search_query) |
            Q(tk_date__icontains=search_query) |
            Q(tk_wk__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(mod_id__mod_code__icontains=search_query) |
            Q(created_at__icontains=search_query)
        )

    paginator = Paginator(tasks, 8)
    page_number = request.GET.get('page', 1)

    try:
        tasks = paginator.page(page_number)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(request, "instructor_templates/manage_instructor_term_note.html",
                  {"tasks": tasks, "search_query": search_query})


def task_pdf(request, search_query=None):
    try:
        if search_query is None:
            search_query = request.GET.get('search', '')

        # Retrieve selected checkboxes IDs
        selected_ids = request.GET.get('selected_ids', '').split(',')
        # Remove empty strings from selected_ids list
        selected_ids = [id for id in selected_ids if id]

        # Fetch modules based on the search query
        tasks = Task.objects.filter(
            Q(tk_name__icontains=search_query) |
            Q(tk_date__icontains=search_query) |
            Q(tk_wk__icontains=search_query) |
            Q(status__icontains=search_query) |
            Q(mod_id__mod_code__icontains=search_query) |
            Q(created_at__icontains=search_query)
        )

        # If selected IDs are provided, export only selected data
        if selected_ids:
            tasks = tasks.filter(lk_id__in=selected_ids)

        # Initialize response
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        p = SimpleDocTemplate(buffer, pagesize=letter)

        # Define table data
        table_data = [['ID', 'Task Name', 'Task Date', 'Week', 'Status', 'Module']]
        for task in tasks:
            table_data.append(
                [task.tk_id, task.tk_name, task.tk_date, task.tk_wk, task.status, task.mod_id.mod_code])

        # Calculate initial column widths based on the length of the header and content
        col_widths = [max(len(str(header)) * 8, max(len(str(row[i])) for row in table_data) * 8) for i, header in
                      enumerate(table_data[0])]

        # Define styles for table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Text color
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid line style
            ('WORDWRAP', (0, 0), (-1, -1)),  # Enable word wrap
        ])

        # Create table and elements for PDF
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(style)
        elements = [table]

        # Build PDF and write to response
        p.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        # Set the PDF content in the response
        response.write(pdf)

        # Set the content-disposition header to inline
        response['Content-Disposition'] = 'inline; filename="term_note_data.pdf"'

    except Exception as e:
        # Handle other exceptions
        response = HttpResponse(f"An error occurred: {str(e)}")

    return response


def task_csv():
    return None


def edit_instructor_task(request, tk_id):
    request.session['tk_id'] = tk_id
    task = Task.objects.get(tk_id=tk_id)
    form = EditTermForm()
    form.fields['tk_name'].initial = task.tk_name
    form.fields['tk_date'].initial = task.tk_date
    form.fields['tk_wk'].initial = task.tk_wk
    form.fields['status'].initial = task.status
    form.fields['mod_id'].initial = task.mod_id

    return render(request, "instructor_templates/edit_instructor_term_note.html", {"form": form, "tk_id": tk_id})


def edit_instructor_task_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        tk_id = request.session.get("tk_id")
        if tk_id is None:
            return HttpResponseRedirect(reverse("manage_instructor_task"))
        form = EditTermForm(request.POST)
        if form.is_valid():
            tk_name = form.cleaned_data["tk_name"]
            tk_date = form.cleaned_data["tk_date"]
            tk_wk = form.cleaned_data["tk_wk"]
            status = form.cleaned_data["status"]
            mod_id = form.cleaned_data["mod_id"]
            sf_id = request.user  # Assuming a way to access the logged-in user

            try:
                task = Task(tk_id=tk_id)
                task.tk_name = tk_name
                task.tk_date = tk_date
                task.tk_wk = tk_wk
                task.status = status
                task.mod_id_id = mod_id
                task.save()
                messages.success(request, "successfully updated")
                return HttpResponseRedirect(reverse("edit_instructor_task", args=[tk_id]))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Update Term Note")
                return HttpResponseRedirect(reverse("edit_instructor_task", args=[tk_id]))

        else:
            return render(request, "instructor_templates/edit_instructor_term_note.html", {"form": form})







def instructor_lesson_plan(request):
    form = AddLessonForm()
    return render(request, "instructor_templates/instructor_lesson_plan.html", {"form": form})


def instructor_lesson_plan_save(request):
    if request.method == "POST":
        form = AddLessonForm(request.POST)
        if form.is_valid():
            st_activity = form.cleaned_data["st_activity"]
            methodology = form.cleaned_data["methodology"]
            media = form.cleaned_data["media"]
            lp_time = form.cleaned_data["lp_time"]
            tk_id = form.cleaned_data["task"]
            sf_id = request.user  # Assuming  have a way to access the logged-in user

            try:
                lesson = Lplan(st_activity=st_activity, methodology=methodology, media=media, lp_time=lp_time,
                               sf_id=sf_id)
                tk_object = Task.objects.get(tk_id=tk_id)
                lesson.tk_id = tk_object
                lesson.save()
                messages.success(request, "successfully added")
                return HttpResponseRedirect(reverse("instructor_lesson_plan"))
            except Exception as e:
                print(e)
                messages.error(request, "Failed to add task")
        else:
            messages.error(request, "Form is not valid")
    else:
        form = AddLessonForm()

    return render(request, "instructor_templates/instructor_lesson_plan.html", {"form": form})


def manage_instructor_lesson_plan(request):
    search_query = request.GET.get('search', '')
    user = request.user
    lessons = Lplan.objects.filter(sf_id=user).order_by('lp_id')

    if search_query:
        lessons = lessons.filter(
            Q(tk_id__tk_name__icontains=search_query) |
            Q(st_activity__icontains=search_query) |
            Q(methodology__icontains=search_query) |
            Q(media__icontains=search_query) |
            Q(lp_time__icontains=search_query) |
            Q(created_at__icontains=search_query)
        )

    paginator = Paginator(lessons, 8)
    page_number = request.GET.get('page', 1)

    try:
        lessons = paginator.page(page_number)
    except EmptyPage:
        lessons = paginator.page(paginator.num_pages)

    return render(request, "instructor_templates/manage_instructor_lesson_plan.html",
                  {"lessons": lessons, "search_query": search_query})


def lesson_pdf(request, search_query=None):
    try:
        if search_query is None:
            search_query = request.GET.get('search', '')

        # Retrieve selected checkboxes IDs
        selected_ids = request.GET.get('selected_ids', '').split(',')
        # Remove empty strings from selected_ids list
        selected_ids = [id for id in selected_ids if id]

        # Fetch modules based on the search query
        lessons = Lplan.objects.filter(
            Q(tk_id__tk_name__icontains=search_query) |
            Q(st_activity__icontains=search_query) |
            Q(methodology__icontains=search_query) |
            Q(media__icontains=search_query) |
            Q(lp_time__icontains=search_query) |
            Q(created_at__icontains=search_query)
        )

        # If selected IDs are provided, export only selected data
        if selected_ids:
            lessons = lessons.filter(lp_id__in=selected_ids)

        # Initialize response
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        p = SimpleDocTemplate(buffer, pagesize=letter)

        # Define table data
        table_data = [['ID', 'Instructor Activity', 'Student Activity', 'Methodology', 'Required Media', 'Time (hrs)']]
        for lesson in lessons:
            table_data.append(
                [lesson.lp_id, lesson.tk_id, lesson.st_activity, lesson.methodology, lesson.media, lesson.lp_time])

        # Calculate initial column widths based on the length of the header and content
        col_widths = [max(len(str(header)) * 8, max(len(str(row[i])) for row in table_data) * 8) for i, header in
                      enumerate(table_data[0])]

        # Define styles for table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Text color
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid line style
            ('WORDWRAP', (0, 0), (-1, -1)),  # Enable word wrap
        ])

        # Create table and elements for PDF
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(style)
        elements = [table]

        # Build PDF and write to response
        p.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        # Set the PDF content in the response
        response.write(pdf)

        # Set the content-disposition header to inline
        response['Content-Disposition'] = 'inline; filename="lesson_plan_data.pdf"'

    except Exception as e:
        # Handle other exceptions
        response = HttpResponse(f"An error occurred: {str(e)}")

    return response


def lesson_csv():
    return None


def edit_instructor_lesson_plan(request, lp_id):
    request.session['lp_id'] = lp_id
    lesson = Lplan.objects.get(lp_id=lp_id)
    form = EditLessonForm()
    form.fields['task'].initial = lesson.tk_id_id
    form.fields['st_activity'].initial = lesson.st_activity
    form.fields['methodology'].initial = lesson.methodology
    form.fields['media'].initial = lesson.media
    form.fields['lp_time'].initial = lesson.lp_time

    return render(request, "instructor_templates/edit_instructor_lesson_plan.html", {"form": form, "lp_id": lp_id})


def edit_instructor_lesson_plan_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        lp_id = request.session.get("lp_id")
        if lp_id is None:
            return HttpResponseRedirect(reverse("manage_instructor_lesson_plan"))
        form = EditLessonForm(request.POST)
        if form.is_valid():
            st_activity = form.cleaned_data["st_activity"]
            methodology = form.cleaned_data["methodology"]
            media = form.cleaned_data["media"]
            lp_time = form.cleaned_data["lp_time"]
            tk_id = form.cleaned_data["task"]
            sf_id = request.user  # Assuming a way to access the logged-in user

            try:
                lesson = Lplan(lp_id=lp_id)
                lesson.st_activity = st_activity
                lesson.methodology = methodology
                lesson.media = media
                lesson.lp_time = lp_time
                lesson.tk_id_id = tk_id
                lesson.save()
                messages.success(request, "successfully updated")
                return HttpResponseRedirect(reverse("edit_instructor_lesson_plan", args=[lp_id]))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Update Lesson Plan")
                return HttpResponseRedirect(reverse("edit_instructor_lesson_plan", args=[lp_id]))

        else:
            return render(request, "instructor_templates/edit_instructor_lesson_plan.html", {"form": form})


def instructor_add_result(request):
    instructor_obj = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(sf_id=instructor_obj)
    batches = Batch.objects.all()

    return render(request, "instructor_templates/instructor_add_result.html",
                  {"subjects": subjects, "batches": batches})


def instructor_save_result(request):
    if request.method != 'POST':
        return HttpResponseRedirect('staff_add_result')
    student_admin_id = request.POST.get('student_list')
    assignment_marks = request.POST.get('assignment_marks')
    exam_marks = request.POST.get('exam_marks')
    sub_id = request.POST.get('subject')

    student_obj = Student.objects.get(admin=student_admin_id)
    subject_obj = Subject.objects.get(sub_id=sub_id)

    try:
        check_exist = StudentResult.objects.filter(sub_id=subject_obj, st_id=student_obj).exists()
        if check_exist:
            result = StudentResult.objects.get(sub_id=subject_obj, st_id=student_obj)
            result.sub_asgn_marks = assignment_marks
            result.sub_exam_marks = exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("instructor_add_result"))
        else:
            result = StudentResult(st_id=student_obj, sub_id=subject_obj, sub_exam_marks=exam_marks,
                                   sub_asgn_marks=assignment_marks)
            result.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect(reverse("instructor_add_result"))
    except:
        messages.error(request, "Failed to Add Result")
        return HttpResponseRedirect(reverse("instructor_add_result"))


@csrf_exempt
def get_students(request):
    sub_id = request.POST.get("subject")
    b_id = request.POST.get("batch")

    subject = Subject.objects.get(sub_id=sub_id)
    batch = Batch.objects.get(b_id=b_id)
    students = Student.objects.filter(c_id=subject.c_id, b_id=batch)
    list_data = []

    for student in students:
        data_small = {"id": student.admin.id, "name": student.admin.first_name + " " + student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def sf_view_attendance(request):
    search_query = request.GET.get('search', '')
    search_id = request.GET.get('searchi', '')
    user = request.user

    attendances = Attendance.objects.filter(sf_id=user).order_by('at_id')

    if search_query:
        attendances = attendances.filter(
            # Q(at_date__icontains=search_query) |
            # Q(status__icontains=search_query) |
            # Q(c_id__c_name__icontains=search_query) |
            Q(status__icontains=search_query)
        )
    if search_id:
        attendances=attendances.filter(
            Q(st_id__st_idNo__icontains=search_id)
        )

    paginator = Paginator(attendances, 8)
    page_number = request.GET.get('page', 1)

    try:
        attendances = paginator.page(page_number)
    except EmptyPage:
        attendances = paginator.page(paginator.num_pages)

    return render(request, "instructor_templates/instructor_view_attendance.html",
                  {"attendances": attendances, "search_query": search_query})


def sf_at_pdf(request, search_query=None):
    try:
        if search_query is None:
            search_query = request.GET.get('search', '')

        user = request.user  # Logged-in instructor user

        # Fetch attendances related to the logged-in instructor
        attendances = Attendance.objects.filter(sf_id=user)

        # If a search query exists, filter by it
        if search_query:
            attendances = attendances.filter(
                Q(at_date__icontains=search_query) |
                Q(status__icontains=search_query) |
                Q(c_id__c_name__icontains=search_query) |
                Q(sub_id__sub_code__icontains=search_query)
            )

        # Initialize response
        response = HttpResponse(content_type='application/pdf')

        # Initialize PDF buffer
        buffer = BytesIO()

        # Create PDF document
        p = SimpleDocTemplate(buffer, pagesize=letter)

        # Define elements for PDF
        elements = []

        # Adding headers and footers
        def add_header_footer(canvas, doc):
            canvas.saveState()

            # Draw images and text for header
            canvas.drawImage('static/dist/img/sl_gov.png', 36, 750, width=60, height=60, mask='auto')
            canvas.drawImage('static/dist/img/touch-icon.png', 36, 690, width=60, height=60, mask='auto')
            canvas.drawImage('static/dist/img/mis.png', 496, 750, width=60, height=60, mask='auto')

            canvas.setFont('Helvetica-Bold', 20)
            canvas.setFillColor(colors.purple)
            canvas.drawString(150, 720, "Technical College - Gampaha")

            at_info = "Student Attendance Data"
            canvas.setFont('Helvetica-Bold', 16)
            canvas.drawString(200, 690, at_info)

            canvas.setFont('Helvetica-Bold', 12)
            canvas.setFillColor(colors.black)

            # Draw user information
            canvas.drawString(200, 660, f"Instructor: {user.get_full_name()}")

            # Draw horizontal line
            canvas.setLineWidth(2)
            canvas.setStrokeColor(colors.darkblue)
            canvas.line(36, 650, 560, 650)

            canvas.restoreState()

        p.addPageTemplates([PageTemplate(id='headerFooter', frames=[Frame(36, 50, 524, 742)])])

        # Define table data
        table_data = [['ID', 'Date', 'Status']]
        for attendance in attendances:
            table_data.append([str(attendance.at_id), str(attendance.at_date), attendance.status])

        # Define styles for table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
            # Add more styles as needed
        ])

        # Create table and add it to the elements
        table = Table(table_data)
        table.setStyle(style)
        elements.append(Spacer(1, 1.9 * inch))  # Add spacer before the table
        elements.append(table)  # Add table below the horizontal line

        # Build the PDF document
        p.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

        # Close the buffer
        buffer.seek(0)
        response.write(buffer.getvalue())
        buffer.close()

        # Set the content-disposition header to inline
        response['Content-Disposition'] = 'inline; filename="student_attendance.pdf"'

        return response

    except Exception as e:
        # Handle other exceptions
        response = HttpResponse(f"An error occurred: {str(e)}")
        return response


def sf_at_csv(request, search_query=None):
    try:
        # Retrieve search query
        if search_query is None:
            search_query = request.GET.get('search', '')

        # Fetch modules based on the search query
        user = request.user

        attendances = Attendance.objects.filter(sf_id=user).order_by('at_id')

        if search_query:
            attendances = attendances.filter(
                Q(at_date__icontains=search_query) |
                Q(status__icontains=search_query) |
                Q(st_id__nic__icontains=search_query) |  # Filter by student NIC
                Q(c_id__c_name__icontains=search_query) |
                Q(sub_id__sub_code__icontains=search_query)
            )

        # Define CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student_attendance.csv"'

        # Write CSV data
        writer = csv.writer(response)
        writer.writerow(['ID', 'Date', 'Status', 'Student ID Number'])  # Write header row

        # Write data rows for searched attendances
        for attendance in attendances:
            writer.writerow([attendance.at_id, attendance.at_date, attendance.status, attendance.st_id.st_idNo])

        return response

    except Exception as e:
        # Handle other exceptions
        response = HttpResponse(f"An error occurred: {str(e)}")
        return response


@csrf_exempt
def staff_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        staff = Staff.objects.get(admin=request.user.id)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
