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
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip
from mistech.face_recognition import recognize_student_face, load_known_face_encodings
from mistech.models import Attendance, Course, Student, Staff, Subject, SessionYr, CustomUser, LeaveReportSf, FeedbackSf
from django.contrib.auth.decorators import login_required
from channels.db import database_sync_to_async
from django.http import StreamingHttpResponse
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404


def instructor_home(request):
    return render(request, "instructor_templates/instructor_home_content.html")


def get_subjects(request):
    c_name = request.GET.get('c_id')
    try:
        # Find the Course instance based on the provided course name
        course = Course.objects.get(c_name=c_name)
        # Retrieve subjects for the given course
        subjects = Subject.objects.filter(c_id=course).values('sub_id', 'sub_name')
        return JsonResponse({'subjects': list(subjects)})
    except Course.DoesNotExist:
        return JsonResponse({'subjects': []})


def mark_absent_students(students, course, subject, session_yr, staff):
    """
    Marks absent students after 2 minutes if their attendance status is not "Present".
    """
    for student in students:
        st_id = student.st_idNo
        # Check if the student's attendance has already been marked as "Present" within the last 2 minutes
        last_attendance = Attendance.objects.filter(
            st_id=student, yr_id=session_yr, created_at__gte=timezone.now() - timezone.timedelta(minutes=2),
            status='Present'
        ).exists()

        if not last_attendance:
            # Mark the student as absent if their attendance status is not "Present"
            Attendance.objects.create(st_id=student, status='Absent', c_id=course, sub_id=subject,
                                       yr_id=session_yr, sf_id=staff.admin)


@login_required
def instructor_take_attendance(request):
    if request.method == 'POST':
        # Retrieve subject, course, and student information from the form
        sub_name = request.POST.get('sub_name')
        c_name = request.POST.get('c_name')
        yr_id = request.POST.get('yr_id')

        try:
            course = Course.objects.get(c_name__iexact=c_name.strip())
            subjects = Subject.objects.filter(sub_name__iexact=sub_name.strip(), c_id=course)

            if subjects.exists():
                subject = subjects.first()
            else:
                return JsonResponse({'status': 'error', 'message': f'Subject with name "{sub_name}" for course "{c_name}" not found.'}, status=400)

            staff = request.user.staff
            session_yr = get_object_or_404(SessionYr, yr_id=yr_id)
            students = Student.objects.filter(c_id=course)

            known_encodings, known_ids = load_known_face_encodings(students)

            for student in students:
                profile_img_path = student.admin.profile_img.path
                if os.path.exists(profile_img_path):
                    try:
                        known_image = face_recognition.load_image_file(profile_img_path)
                        known_encoding = face_recognition.face_encodings(known_image)[0]
                        known_encodings.append(known_encoding)
                        known_ids.append({'id': student.st_idNo, 'last_marked_time': None})
                    except Exception as e:
                        print(f"Error processing image for student {student.st_idNo}: {e}")
                        continue
                else:
                    print(f"Profile image not found for student {student.st_idNo}")

            last_marked_times = {student_info['id']: None for student_info in known_ids}
            video_capture = cv2.VideoCapture(0)
            attendance_status = 'Absent'
            st_idNo = 'Please register to the system'  # Set a default value for st_idNo
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
                            # Check if attendance has already been marked as "Present" within the last 2 minutes
                            existing_attendance = Attendance.objects.filter(
                                st_id=student, yr_id=session_yr, created_at__gte=timezone.now() - timezone.timedelta(minutes=2),
                                status='Present'
                            ).exists()

                            if not existing_attendance:
                                # Student is recognized, mark attendance and update last_marked_time
                                attendance_status = 'Present'
                                st_idNo = student_info['id']
                                student_info['last_marked_time'] = datetime.now()
                                recognized_st_info = student_info
                                break
                            else:
                                # Student's attendance has already been marked as "Present" within the last 2 minutes
                                attendance_status = 'Already Marked'
                                st_idNo = student_info['id']
                                recognized_st_info = student_info
                                break
                    else:
                        # Unknown face
                        attendance_status = 'Unknown'

            video_capture.release()

            if st_idNo == 'Please register to the system':
                return JsonResponse({'status': 'error','message': 'Student not found in the system. Please register to the system.'})
            elif attendance_status == 'Already Marked':
                return JsonResponse({'status': 'error', 'message': f'Student {st_idNo} attendance has already been taken within the last two minutes.'})
            elif attendance_status == 'Present':
                student = Student.objects.get(st_idNo=st_idNo)
                session_yr = SessionYr.object.get(yr_id=yr_id)

                if not Student.objects.filter(st_idNo=st_idNo, yr_id=session_yr).exists():
                    return JsonResponse({'status': 'warning', 'message': f'Student {st_idNo} is not registered for the selected session year.'})

                Attendance.objects.create(st_id=student, status='Present', c_id=course, sub_id=subject, yr_id=session_yr, sf_id=staff.admin)

                # Call mark_absent_students to mark absent students after 2 minutes
                mark_absent_students(students, course, subject, session_yr, staff)

                return JsonResponse({'status': 'success', 'message': f'Student {st_idNo} attendance marked as {attendance_status}.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Unable to recognize the student.'})

        except (Course.DoesNotExist, Subject.DoesNotExist, Staff.DoesNotExist, Student.DoesNotExist, SessionYr.DoesNotExist) as e:
            print("Error: ", e)
            return JsonResponse({'status': 'warning', 'message': 'Invalid course details or student not found.'}, status=400)

    else:
        staff = Staff.objects.all()
        subject = Subject.objects.all()
        course = Course.objects.all()
        session_yr = SessionYr.object.all()
        return render(request, 'instructor_templates/instructor_take_attendance.html', {'staff': staff, 'subject': subject, 'course': course, 'session_yr': session_yr})




def instructor_apply_leave(request):
    instructor_obj = Staff.objects.get(admin=request.user.id)
    lv_data = LeaveReportSf.objects.filter(sf_id=instructor_obj)

    return render(request, "instructor_templates/instructor_apply_leave.html", {"lv_data": lv_data})


def instructor_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("instructor_apply_leave"))
    else:
        lrs_date = request.POST.get("lrs_date")
        lrs_msg = request.POST.get("lrs_msg")

        instructor_obj = Staff.objects.get(admin=request.user.id)
        try:
            lv_report = LeaveReportSf(sf_id=instructor_obj, lrs_date=lrs_date, lrs_msg=lrs_msg, lrs_status=0)
            lv_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("instructor_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("instructor_apply_leave"))


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
