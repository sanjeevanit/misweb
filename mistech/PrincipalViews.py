import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from mistech.models import Student, Course, Subject, CustomUser, Attendance, LeaveReportS, FeedBackS, LeaveReportSf


def principal_home(request):
    return render(request, "principal_templates/principal_home_content.html")


def staff_leave_view(request):
    leaves = LeaveReportSf.objects.all()
    return render(request, "principal_templates/staff_leave_view.html", {"leaves": leaves})


def staff_approve_leave(request,lrs_id):
    leave=LeaveReportSf.objects.get(lrs_id=lrs_id)
    leave.lrs_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_disapprove_leave(request,lrs_id):
    leave=LeaveReportSf.objects.get(lrs_id=lrs_id)
    leave.lrs_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def principal_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "principal_templates/principal_profile.html", {"user": user})


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