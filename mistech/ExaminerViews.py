import csv

import face_recognition
import cv2
import json
import dlib
import numpy as np
import datetime
import asyncio
import os
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip
from mistech.face_recognition import recognize_student_face, load_known_face_encodings
from mistech.models import AttendanceE, Course, Student, Staff, Subject, SessionYr, CustomUser, LeaveReportSf, \
    FeedbackSf, Batch
from django.contrib.auth.decorators import login_required
from channels.db import database_sync_to_async
from django.http import StreamingHttpResponse
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa


def examiner_home(request):
    return render(request, "examiner_templates/examiner_home_content.html")


def get_subjects_ex(request):
    c_name = request.GET.get('c_id')
    try:
        # Find the Course instance based on the provided course name
        course = Course.objects.get(c_name=c_name)
        # Retrieve subjects for the given course
        subjects = Subject.objects.filter(c_id=course).values('sub_id', 'sub_name')

        return JsonResponse({'subjects': list(subjects)})
    except Course.DoesNotExist:
        return JsonResponse({'subjects': []})


def get_batches_ex(request):
    c_name = request.GET.get('c_id')
    try:
        # Find the Course instance based on the provided course name
        course = Course.objects.get(c_name=c_name)
        # Retrieve subjects for the given course
        batches = Batch.objects.filter(c_id=course).values('b_id', 'b_code')

        return JsonResponse({'batches': list(batches)})
    except Course.DoesNotExist:
        return JsonResponse({'batches': []})


def mark_absent_students(students, course, subject, batch, session_yr, staff, ex_name):
    """
    Marks absent students after 2 minutes if their attendance status is not "Present".
    """
    for student in students:
        st_id = student.st_idNo
        # Check if the student's attendance has already been marked as "Present" within the last 2 minutes
        last_attendance = AttendanceE.objects.filter(
            st_id=student, c_id=course, b_id=batch, yr_id=session_yr, ex_name=ex_name,
            created_at__gte=timezone.now() - timezone.timedelta(minutes=2),
            status='Present'
        ).exists()

        if not last_attendance:
            # Mark the student as absent if their attendance status is not "Present"
            AttendanceE.objects.create(st_id=student, status='Absent', c_id=course, sub_id=subject, b_id=batch,
                                      yr_id=session_yr, sf_id=staff.admin, ex_name=ex_name)


@login_required
def examiner_take_attendance(request):
    if request.method == 'POST':
        sub_name = request.POST.get('sub_name')
        c_name = request.POST.get('c_name')
        b_code = request.POST.get('b_code')
        yr_id = request.POST.get('yr_id')
        ex_name = request.POST.get('ex_name')


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
                            existing_attendance = AttendanceE.objects.filter(
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

                AttendanceE.objects.create(st_id=student, status='Present', c_id=course, sub_id=subject, b_id=batch,
                                          yr_id=session_yr, sf_id=staff.admin, ex_name=ex_name)

                mark_absent_students(students, course, subject, batch, session_yr, staff, ex_name)

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
        return render(request, 'examiner_templates/examiner_take_attendance.html',
                      {'staff': staff, 'subject': subject, 'batch': batch, 'course': course, 'session_yr': session_yr})


def examiner_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "examiner_templates/examiner_profile.html", {"user": user})


def examiner_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("examiner_profile"))
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
            return HttpResponseRedirect(reverse("examiner_profile"))
        except:
            messages.error(request, "Failed to Updated Profile")
            return HttpResponseRedirect(reverse("examiner_profile"))


def examiner_view_attendance(request, export_all=False):
    search_exam = request.GET.get('search', '')

    if search_exam:
        exams = AttendanceE.objects.filter(
            Q(ex_name__icontains=search_exam) |
            Q(ae_date__icontains=search_exam) |
            Q(created_at__icontains=search_exam),
        ).order_by('ae_id')
    elif export_all:
        exams = AttendanceE.objects.all().order_by('ae_id')
    else:
        exams = AttendanceE.objects.all().order_by('ae_id')

    paginator = Paginator(exams, 8)
    page_number = request.GET.get('page', 1)

    try:
        exams = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseNotFound("Page not found")

    return render(request, "examiner_templates/examiner_view_attendance.html", {"exam": exams, "search_exam": search_exam})



def get_subjects(request):
    c_id = request.GET.get('c_id')  # Changed variable name to match the parameter name
    try:
        # Find the Course instance based on the provided course ID
        course = Course.objects.get(pk=c_id)  # Using pk (primary key) to retrieve the course
        # Retrieve subjects for the given course
        subjects = Subject.objects.filter(c_id=course).values('sub_id', 'sub_name')

        return JsonResponse({'subjects': list(subjects)})
    except Course.DoesNotExist:
        return JsonResponse({'subjects': []})





def generate_daily_exam_report(request):
    ae_date_str = request.GET.get('ae_date')

    # Check if ae_date_str is not None and parse it
    if ae_date_str is not None:
        ae_date = timezone.make_aware(datetime.strptime(ae_date_str, '%Y-%m-%d'))
    else:
        ae_date = None

    c_id = request.GET.get('c_name')  # Get the selected course ID
    sub_id = request.GET.get('subject_name')  # Get the selected subject ID

    # Fetch distinct exam names based on the selected date, course, and subject
    attendance_data = AttendanceE.objects.all()  # Start with all objects

    # Apply filters only if the values are not None
    if ae_date is not None:
        attendance_data = attendance_data.filter(ae_date=ae_date)
    if c_id is not None:
        attendance_data = attendance_data.filter(c_id=c_id)
    if sub_id is not None:
        attendance_data = attendance_data.filter(sub_id=sub_id)

    # Get distinct exam names from filtered query set
    exam_names = attendance_data.values('ex_name').distinct().values_list('ex_name', flat=True)
    print("Exam Names from Database Query:", exam_names)
    # Fetch course data from the database
    courses = Course.objects.all()

    context = {
        'courses': courses,
        'ae_date': ae_date,
        'exam_names': exam_names,
    }

    return render(request, "examiner_templates/exam_daily_attendance_report.html", context)








def exam_pdf(request):
    template_path = 'pdf_template.html'
    ae_date = request.GET.get('ae_date')
    ex_name = request.GET.get('ex_name')
    attendance_data = AttendanceE.objects.filter(ae_date=ae_date, ex_name=ex_name)

    context = {'attendance_data': attendance_data}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="attendance_report_{ae_date}_{ex_name}.pdf"'

    # Render template
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def exam_csv(request):
    ae_date = request.GET.get('ae_date')
    ex_name = request.GET.get('ex_name')
    attendance_data = AttendanceE.objects.filter(ae_date=ae_date, ex_name=ex_name)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_report_{ae_date}_{ex_name}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Attendance Status'])

    for record in attendance_data:
        writer.writerow([record.st_id, record.status])

    return response





def exam_other_attendance_report():
    return None


