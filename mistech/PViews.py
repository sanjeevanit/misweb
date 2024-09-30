import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from mistech.models import Student, Course, Subject, CustomUser, Attendance, LeaveReportS, FeedBackS, LeaveReportSf, \
    Staff


def p_home(request):
    student_count1 = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    subject_count = Subject.objects.all().count()
    course_count = Course.objects.all().count()

    course_all = Course.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []
    for course in course_all:
        subjects=Subject.objects.filter(c_id=course.c_id).count()
        students=Student.objects.filter(c_id=course.c_id).count()
        course_name_list.append(course.c_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all = Subject.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subjects_all:
        course=Course.objects.get(c_id=subject.c_id.c_id)
        student_count=Student.objects.filter(c_id=course.c_id).count()
        subject_list.append(subject.sub_code)
        student_count_list_in_subject.append(student_count)

    staffs=Staff.objects.all()
    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subject.objects.filter(sf_id=staff.admin.id)
        attendance=Attendance.objects.filter(sub_id__in=subject_ids).count()
        leaves=LeaveReportSf.objects.filter(sf_id=staff.sf_id,lrs_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all=Student.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=Attendance.objects.filter(st_id=student.st_id,status="Present").count()
        absent=Attendance.objects.filter(st_id=student.st_id,status="Absent").count()
        leaves=LeaveReportS.objects.filter(st_id=student.st_id,lr_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves+absent)
        student_name_list.append(student.admin.username)
    return render(request, "p_templates/p_home_content.html",{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})


def student_view_attendance(request):
    student = Student.objects.get(admin=request.user.id)
    course = student.c_id
    subject = Subject.objects.filter(c_id=course)
    return render(request, "student_templates/student_view_attendance.html", {"subject": subject})


def staff_apply_leave(request):
    leaves = LeaveReportSf.objects.all()
    return render(request, "p_templates/staff_leave.html", {"leaves": leaves})


def staff_approve(request, lrs_id):
    leave = LeaveReportSf.objects.get(lrs_id=lrs_id)
    leave.lrs_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_apply_leave"))


def staff_disapprove(request, lrs_id):
    leave = LeaveReportSf.objects.get(lrs_id=lrs_id)
    leave.lrs_status = 2
    leave.reason_lv
    leave.save()



    return HttpResponseRedirect(reverse("staff_apply_leave"))


def student_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        lr_date = request.POST.get("lr_date")
        lr_msg = request.POST.get("lr_msg")

        st_obj = Student.objects.get(admin=request.user.id)
        try:
            lv_report = LeaveReportS(st_id=st_obj, lr_date=lr_date, lr_msg=lr_msg, lr_status=0)
            lv_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))



def principal_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "p_templates/principal_profile.html", {"user": user})


def principal_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("principal_profile"))
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
            return HttpResponseRedirect(reverse("principal_profile"))
        except:
            messages.error(request, "Failed to Updated Profile")
            return HttpResponseRedirect(reverse("principal_profile"))