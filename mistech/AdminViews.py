import json
import csv
import logging


from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound, \
    HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, When, Case, IntegerField
from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.platypus.frames import Frame
from django.http import FileResponse
from django.db import IntegrityError, transaction
from reportlab.lib.units import inch, cm
from reportlab.lib.utils import ImageReader
from django.utils import timezone

from mistech.form import AddTradeForm, EditTradeForm, AddCourseForm, AddSubjectForm, EditSubjectForm, EditCourseForm, \
    AddStudentForm, AddStaffForm, EditStaffForm, EditStudentForm, AddBatchForm, EditBatchForm, AddModuleForm, \
    EditModuleForm
from mistech.models import CustomUser, Subject, Trade, Course, Student, Staff, SessionYr, FeedBackS, FeedbackSf, \
    LeaveReportSf, LeaveReportS, Attendance, Batch, Module, Payment, NotificationSf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, Spacer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@login_required(login_url='/')
def admin_home(request):
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


    student_payment_data = []
    for student in students_all:
        # Counting payments for each student
        payments_count = Payment.objects.filter(st_id=student).count()
        payment_status = "Paid" if payments_count > 0 else "Unpaid"
        student_payment_data.append({"student_name": student.admin.username, "payment_status": payment_status})


    return render(request, "admin_templates/home_content.html", {
        "student_count": student_count1,
        "staff_count": staff_count,
        "subject_count": subject_count,
        "course_count": course_count,
        "course_name_list": course_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_course": student_count_list_in_course,
        "student_count_list_in_subject": student_count_list_in_subject,
        "subject_list": subject_list,
        "staff_name_list": staff_name_list,
        "attendance_present_list_staff": attendance_present_list_staff,
        "attendance_absent_list_staff": attendance_absent_list_staff,
        "student_name_list": student_name_list,
        "attendance_present_list_student": attendance_present_list_student,
        "attendance_absent_list_student": attendance_absent_list_student,
        "student_payment_data": student_payment_data  # New data for student payment status
    })

def add_trade(request):
    form = AddTradeForm
    return render(request, "admin_templates/add_trade.html", {"form": form})


def add_trade_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddTradeForm(request.POST)
        if form.is_valid():
            trade = form.cleaned_data["tr_name"]
            try:
                trade_model = Trade(tr_name=trade)
                trade_model.save()
                messages.success(request, "Successfully Added")
                return HttpResponseRedirect(reverse("add_trade"))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Add Trade")
                return HttpResponseRedirect(reverse("add_trade"))
        else:
            form = AddTradeForm(request.POST)
            return render(request, "admin_templates/add_trade.html", {"form": form})


@csrf_exempt
def check_tradename_exist(request):
    tr_name = request.POST.get("tr_name", "").strip()  # Remove leading/trailing whitespaces
    if tr_name:
        # Check if a similar trade name exists (case-insensitive and ignoring spaces)
        trade_exists = Trade.objects.filter(
            Q(tr_name__icontains=tr_name) | Q(tr_name__icontains=tr_name.replace(" ", ""))
        ).exists()
        return JsonResponse({'exists': trade_exists})  # Return the result as JSON
    else:
        return JsonResponse({'exists': False})  # Return False if no trade name provided


def manage_trade(request):
    search_tr = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    if search_tr:
        trade = Trade.objects.filter(
            Q(tr_name__icontains=search_tr) |
            Q(created_at__icontains=search_tr)
        ).order_by('tr_id')
    else:
        trade = Trade.objects.all().order_by('tr_id')
    paginator = Paginator(trade, 8)
    try:
        page = int(page)
    except ValueError:
        print("Invalid page number")
        return HttpResponseBadRequest("Invalid page number")
    try:
        trade = paginator.page(page)
    except EmptyPage:
        print("Page not found")
        return HttpResponseNotFound("Page not found")
    return render(request, "admin_templates/manage_trade.html", {"trade": trade, "search_tr": search_tr})


def tr_pdf(request, search_tr):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="trade_data.pdf"'

    # Create a PDF file
    p = canvas.Canvas(response)
    p.drawString(100, 800, f'Searched Trade Data for: {search_tr}')
    trade = Trade.objects.filter(
        Q(tr_name__icontains=search_tr) |
        Q(created_at__icontains=search_tr)
    ).order_by('tr_id')

    y_position = 750
    for trade in trade:
        p.drawString(100, y_position,
                     f'Trade Name: {trade.tr_name}, Created At: {trade.created_at}')
        y_position -= 20

    p.showPage()
    p.save()
    print(trade.count())
    return response


def tr_csv(request, search_tr):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="trade_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Trade Name', 'Type', 'Created At'])

    trade = Trade.objects.filter(
        Q(tr_name__icontains=search_tr) |
        Q(created_at__icontains=search_tr)
    ).order_by('tr_id')

    for trade in trade:
        writer.writerow([trade.tr_name, trade.created_at])

    return response


def edit_trade(request, tr_id):
    request.session['tr_id'] = tr_id
    trade = Trade.objects.get(tr_id=tr_id)
    form = EditTradeForm()
    form.fields['tr_name'].initial = trade.tr_name
    return render(request, "admin_templates/edit_trade.html", {"form": form, "tr_id": tr_id})


@transaction.atomic
def edit_trade_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        tr_id = request.session.get("tr_id")
        if tr_id is None:
            return HttpResponseRedirect(reverse("manage_trade"))

        form = EditTradeForm(request.POST)
        if form.is_valid():
            tr_name = form.cleaned_data["tr_name"]

            try:
                # Retrieve the trade object to update
                trade = Trade.objects.get(tr_id=tr_id)
                trade.tr_name = tr_name
                trade.save()
                messages.success(request, "Successfully Updated")
                return HttpResponseRedirect(reverse("edit_trade", kwargs={"tr_id": tr_id}))
            except Trade.DoesNotExist:
                return HttpResponse("Error: Trade does not exist", status=400)
            except IntegrityError as e:
                # Handle integrity constraint violations (e.g., unique constraint)
                messages.error(request, "Error: Integrity constraint violation")
                return HttpResponseRedirect(reverse("edit_trade", kwargs={"tr_id": tr_id}))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Update Trade")
                return HttpResponseRedirect(reverse("edit_trade", kwargs={"tr_id": tr_id}))
        else:
            # If the form is not valid, re-render the edit trade form with validation errors
            return render(request, "admin_templates/edit_trade.html", {"form": form, "tr_id": tr_id})


def get_trade_names(request):
    trade_names = list(Trade.objects.values_list('tr_id', 'tr_name'))
    return JsonResponse({'trade_names': trade_names})


def add_course(request):
    form = AddCourseForm()
    return render(request, "admin_templates/add_course.html", {"form": form})


def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddCourseForm(request.POST)
        if form.is_valid():
            c_name = form.cleaned_data["c_name"]
            c_code = form.cleaned_data["c_code"]
            c_type = form.cleaned_data["c_type"]
            c_duration = form.cleaned_data["c_duration"]
            c_qualification = form.cleaned_data["c_qualification"]
            tr_id = form.cleaned_data["trade"]
            try:
                course = Course(c_name=c_name, c_code=c_code, c_type=c_type, c_duration=c_duration,
                                c_qualification=c_qualification)
                trade_object = Trade.objects.get(tr_id=tr_id)
                course.tr_id = trade_object
                course.save()
                messages.success(request, "Successfully Added Course")
                return HttpResponseRedirect(reverse("add_course"))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Add Course")
                return HttpResponseRedirect(reverse("add_course"))
        else:
            form = AddCourseForm(request.POST)
            return render(request, "admin_templates/add_course.html", {"form": form})


@csrf_exempt
def check_coursename_exist(request):
    c_name = request.POST.get("c_name")
    user_obj = Course.objects.filter(c_name=c_name).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def manage_course(request, export_all=False):
    search_query = request.GET.get('search', '')

    if search_query:
        courses = Course.objects.filter(
            Q(c_name__icontains=search_query) |
            Q(c_code__icontains=search_query) |
            Q(c_type__icontains=search_query) |
            Q(created_at__icontains=search_query),
        ).order_by('c_id')
    elif export_all:
        courses = Course.objects.all().order_by('c_id')
    else:
        courses = Course.objects.all().order_by('c_id')

    paginator = Paginator(courses, 8)
    page_number = request.GET.get('page', 1)

    try:
        courses = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseNotFound("Page not found")

    return render(request, "admin_templates/manage_course.html", {"course": courses, "search_query": search_query})


def c_pdf(request, search_query=None):
    try:
        if search_query is None:
            search_query = request.GET.get('search', '')

        # Retrieve selected checkboxes IDs
        selected_ids = request.GET.get('selected_ids', '').split(',')
        # Remove empty strings from selected_ids list
        selected_ids = [id for id in selected_ids if id]

        # Initialize response
        response = HttpResponse(content_type='application/pdf')

        buffer = BytesIO()
        p = SimpleDocTemplate(buffer, pagesize=letter)

        table_data = [['ID', 'Course Name', 'Course Code', 'Type']]

        # Fetch courses based on the search query
        courses = Course.objects.filter(
            Q(c_name__icontains=search_query) |
            Q(c_code__icontains=search_query) |
            Q(c_type__icontains=search_query)
        ).order_by('c_id')

        # If selected IDs are provided, export only selected data
        if selected_ids:
            courses = courses.filter(c_id__in=selected_ids)

        # Add unselected courses matching the search query to the table data
        for course in courses:
            if course.c_id not in selected_ids:  # Check if the course is not selected
                table_data.append([course.c_id, course.c_name, course.c_code, course.c_type])

        # Define table style and build PDF
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Create table and elements for PDF
        table = Table(table_data)
        table.setStyle(style)
        elements = [table]

        # Build PDF and write to response
        p.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        # Set the PDF content in the response
        response.write(pdf)

        # Set the content-disposition header to inline
        response['Content-Disposition'] = 'inline; filename="course_data.pdf"'

    except Exception as e:
        # Handle other exceptions
        response = HttpResponse(f"An error occurred: {str(e)}")

    return response


def c_csv(request):
    search_query = request.GET.get('search_query', '')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=course_data.xlsx'

    workbook = Workbook()
    worksheet = workbook.active

    header_row = ['COURSE ID', 'COURSE NAME', 'COURSE CODE', 'TYPE']
    for cell_value in header_row:
        cell = worksheet.cell(row=1, column=header_row.index(cell_value) + 1, value=cell_value)
        cell.font = Font(bold=True)

    courses = Course.objects.filter(
        Q(c_name__icontains=search_query) |
        Q(c_code__icontains=search_query) |
        Q(c_type__icontains=search_query)
    ).order_by('c_id')

    for course in courses:
        worksheet.append([course.c_id, course.c_name, course.c_code, course.c_type])

    workbook.save(response)
    return response


def edit_course(request, c_id):
    request.session['c_id'] = c_id
    course = Course.objects.get(c_id=c_id)
    form = EditCourseForm()
    form.fields['c_name'].initial = course.c_name
    form.fields['c_code'].initial = course.c_code
    form.fields['c_type'].initial = course.c_type
    form.fields['c_duration'].initial = course.c_duration
    form.fields['c_qualification'].initial = course.c_qualification
    form.fields['trade'].initial = course.tr_id_id
    return render(request, "admin_templates/edit_course.html", {"form": form, "c_id": c_id})


def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        c_id = request.session.get("c_id")
        if c_id == None:
            return HttpResponseRedirect(reverse("manage_course"))
        form = EditCourseForm(request.POST)
        if form.is_valid():
            c_name = form.cleaned_data["c_name"]
            c_code = form.cleaned_data["c_code"]
            c_type = form.cleaned_data["c_type"]
            c_duration = form.cleaned_data["c_duration"]
            c_qualification = form.cleaned_data["c_qualification"]
            tr_id = form.cleaned_data["trade"]
            try:
                course = Course(c_id=c_id)
                course.c_name = c_name
                course.c_code = c_code
                course.c_type = c_type
                course.c_duration = c_duration
                course.c_qualification = c_qualification
                trade_object = Trade.objects.get(tr_id=tr_id)
                course.tr_id = trade_object
                course.save()
                messages.success(request, "Successfully Updated")
                return HttpResponseRedirect(reverse("edit_course", kwargs={"c_id": c_id}))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Update Course")
                return HttpResponseRedirect(reverse("edit_course", kwargs={"c_id": c_id}))
        else:
            form = EditCourseForm(request.POST)
            return render(request, "admin_templates/edit_course.html", {"form": form, "c_id": c_id})


def get_course_names(request):
    course_names = list(Course.objects.values_list('c_id', 'c_name'))
    return JsonResponse({'course_names': course_names})


def get_staff_idnos(request):
    staff_ids = list(Staff.objects.values_list('sf_id', 'sf_idNo'))
    return JsonResponse({'staff_ids': staff_ids})


@csrf_exempt
def check_subjectname_exist(request):
    sub_name = request.POST.get("sub_name")
    user_obj = Subject.objects.filter(sub_name=sub_name).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def add_subject(request):
    form = AddSubjectForm()
    return render(request, "admin_templates/add_subject.html", {"form": form})


def add_subject_save(request):
    if request.method == "POST":
        form = AddSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Added")
            return HttpResponseRedirect(reverse("add_subject"))
        else:
            messages.error(request, "Failed To Add Subject")
    else:
        form = AddSubjectForm()
    return render(request, "admin_templates/add_subject.html", {"form": form})


def manage_subject(request):
    search_sub = request.GET.get('search', '')
    if search_sub:
        subject = Subject.objects.filter(
            Q(sub_name__icontains=search_sub) |
            Q(sub_code__icontains=search_sub)
        )
    else:
        subject = Subject.objects.all()
    return render(request, "admin_templates/manage_subject.html", {"subject": subject})


def get_staff_ids(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    staff_ids = subject.staff_set.values_list('sf_idNo', flat=True)
    print("Staff ID Numbers:", list(staff_ids))
    return JsonResponse(list(staff_ids), safe=False)


def edit_subject(request, sub_id):
    request.session['sub_id'] = sub_id
    subject = Subject.objects.get(sub_id=sub_id)
    form = EditSubjectForm(instance=subject)
    return render(request, "admin_templates/edit_subject.html", {"form": form, "sub_id": sub_id})


def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        sub_id = request.session.get("sub_id")
        if sub_id == None:
            return HttpResponseRedirect(reverse("manage_subject"))
        form = EditSubjectForm(request.POST)
        if form.is_valid():
            sub_name = form.cleaned_data["sub_name"]
            sub_code = form.cleaned_data["sub_code"]
            c_id = form.cleaned_data["c_id"]
            sf_id = form.cleaned_data["sf_id"]
            try:
                subject = Subject(sub_id=sub_id)
                subject.sub_name = sub_name
                subject.sub_code = sub_code
                course_object = Course.objects.get(c_id=c_id)
                subject.c_id = course_object
                staff_object = Staff.objects.get(sf_id=sf_id)
                subject.sf_id = staff_object
                subject.save()
                messages.success(request, "Successfully Updated")
                return HttpResponseRedirect(reverse("edit_subject", kwargs={"sub_id": sub_id}))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Update Subject")
                return HttpResponseRedirect(reverse("edit_subject", kwargs={"sub_id": sub_id}))
        else:
            form = EditSubjectForm(request.POST)
            return render(request, "admin_templates/edit_subject.html", {"form": form, "sub_id": sub_id})


def add_student(request):
    form = AddStudentForm()
    return render(request, "admin_templates/add_student.html", {"form": form})


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            profile_img = form.cleaned_data["profile_img"]
            first_name = form.cleaned_data["first_name"]
            middle_name = form.cleaned_data["middle_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            dob = form.cleaned_data["dob"]
            adrz = form.cleaned_data["adrz"]
            gender = form.cleaned_data["gender"]
            nic = form.cleaned_data["nic"]
            st_idNo = form.cleaned_data["st_idNo"]
            nationality = form.cleaned_data["nationality"]
            civil_status = form.cleaned_data["civil_status"]
            mobileNo = form.cleaned_data["mobileNo"]
            resiNo = form.cleaned_data["resiNo"]
            prof_qualification = form.cleaned_data["prof_qualification"]
            other_qualification = form.cleaned_data["other_qualification"]
            guardian_name = form.cleaned_data["guardian_name"]
            guardian_contNo = form.cleaned_data["guardian_contNo"]
            yr_id = form.cleaned_data["yr_id"]
            edu_qualification = form.cleaned_data["edu_qualification"]
            b_id = form.cleaned_data["batch"]
            tr_id = form.cleaned_data["trade"]
            c_id = form.cleaned_data["course"]

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      last_name=last_name, first_name=first_name, user_type=3,
                                                      profile_img=profile_img)
                user.student.middle_name = middle_name
                user.student.dob = dob
                user.student.adrz = adrz
                user.student.gender = gender
                user.student.nic = nic
                user.student.st_idNo = st_idNo
                user.student.nationality = nationality
                user.student.civil_status = civil_status
                user.student.mobileNo = mobileNo
                user.student.resiNo = resiNo
                user.student.edu_qualification = edu_qualification
                user.student.prof_qualification = prof_qualification
                user.student.other_qualification = other_qualification
                user.student.guardian_name = guardian_name
                user.student.guardian_contNo = guardian_contNo
                yr_object = SessionYr.object.get(yr_id=yr_id)
                user.student.yr_id = yr_object
                batch_object = Batch.objects.get(b_id=b_id)
                user.student.b_id = batch_object
                trade_object = Trade.objects.get(tr_id=tr_id)
                user.student.tr_id = trade_object
                course_object = Course.objects.get(c_id=c_id)
                user.student.c_id = course_object

                user.save()
                messages.success(request, "Successfully Added")
                return HttpResponseRedirect(reverse("add_student"))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            return render(request, "admin_templates/add_student.html", {"form": form})


def manage_student(request):
    student = Student.objects.all()
    return render(request, "admin_templates/manage_student.html", {"student": student})


def edit_student(request, st_id):
    request.session['st_id'] = st_id
    student = Student.objects.get(st_id=st_id)
    form = EditStudentForm()

    form.fields['profile_img'].initial = student.admin.profile_img.url
    # form.fields['profile_img'].initial = student.admin.profile_img
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['middle_name'].initial = student.middle_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['email'].initial = student.admin.email
    form.fields['dob'].initial = student.dob
    form.fields['adrz'].initial = student.adrz
    form.fields['gender'].initial = student.gender
    form.fields['nic'].initial = student.nic
    form.fields['st_idNo'].initial = student.st_idNo
    form.fields['nationality'].initial = student.nationality
    form.fields['civil_status'].initial = student.civil_status
    form.fields['mobileNo'].initial = student.mobileNo
    form.fields['resiNo'].initial = student.resiNo
    form.fields['edu_qualification'].initial = student.edu_qualification
    form.fields['prof_qualification'].initial = student.prof_qualification
    form.fields['other_qualification'].initial = student.other_qualification
    form.fields['guardian_name'].initial = student.guardian_name
    form.fields['guardian_contNo'].initial = student.guardian_contNo
    form.fields['yr_id'].initial = student.yr_id_id
    form.fields['batch'].initial = student.b_id_id
    form.fields['trade'].initial = student.tr_id_id
    form.fields['course'].initial = student.c_id_id
    return render(request, "admin_templates/edit_student.html",
                  {"form": form, "st_id": st_id, "username": student.admin.username, "user_profile_img": student.admin.profile_img.url})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        st_id = request.session.get("st_id")
        if st_id == None:
            return HttpResponseRedirect(reverse("manage_student"))
        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            profile_img = form.cleaned_data["profile_img"]
            first_name = form.cleaned_data["first_name"]
            middle_name = form.cleaned_data["middle_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            dob = form.cleaned_data["dob"]
            adrz = form.cleaned_data["adrz"]
            gender = form.cleaned_data["gender"]
            nic = form.cleaned_data["nic"]
            st_idNo = form.cleaned_data["st_idNo"]
            nationality = form.cleaned_data["nationality"]
            civil_status = form.cleaned_data["civil_status"]
            mobileNo = form.cleaned_data["mobileNo"]
            resiNo = form.cleaned_data["resiNo"]
            prof_qualification = form.cleaned_data["prof_qualification"]
            other_qualification = form.cleaned_data["other_qualification"]
            guardian_name = form.cleaned_data["guardian_name"]
            guardian_contNo = form.cleaned_data["guardian_contNo"]
            edu_qualification = form.cleaned_data["edu_qualification"]
            yr_id = form.cleaned_data["yr_id"]
            b_id = form.cleaned_data["batch"]
            tr_id = form.cleaned_data["trade"]
            c_id = form.cleaned_data["course"]

            try:
                student = Student.objects.get(st_id=st_id)
                student.middle_name = middle_name
                student.dob = dob
                student.adrz = adrz
                student.gender = gender
                student.nic = nic
                student.st_idNo = st_idNo
                student.nationality = nationality
                student.civil_status = civil_status
                student.mobileNo = mobileNo
                student.resiNo = resiNo
                student.edu_qualification = edu_qualification
                student.prof_qualification = prof_qualification
                student.other_qualification = other_qualification
                student.guardian_name = guardian_name
                student.guardian_contNo = guardian_contNo
                yr_object = SessionYr.object.get(yr_id=yr_id)
                student.yr_id = yr_object
                batch_object = Batch.objects.get(b_id=b_id)
                student.b_id = batch_object
                tr_object = Trade.objects.get(tr_id=tr_id)
                student.tr_id = tr_object
                c_object = Course.objects.get(c_id=c_id)
                student.c_id = c_object
                user = CustomUser.objects.get(id=student.admin.id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.profile_img = profile_img
                user.save()
                student.save()
                del request.session['st_id']
                messages.success(request, "Successfully Updated")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"st_id": st_id}))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Update")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"st_id": st_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Student.objects.get(st_id=st_id)
            return render(request, "admin_templates/edit_student.html",
                          {"form": form, "st_id": st_id, "username": student.admin.username})


def add_staff(request):
    form = AddStaffForm()
    return render(request, "admin_templates/add_staff.html", {"form": form})


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStaffForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid. Form data:", form.cleaned_data)
            profile_img = form.cleaned_data["profile_img"]
            first_name = form.cleaned_data["first_name"]
            middle_name = form.cleaned_data["middle_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            dob = form.cleaned_data["dob"]
            adrz = form.cleaned_data["adrz"]
            gender = form.cleaned_data["gender"]
            nic = form.cleaned_data["nic"]
            sf_idNo = form.cleaned_data["sf_idNo"]
            nationality = form.cleaned_data["nationality"]
            civil_status = form.cleaned_data["civil_status"]
            mobileNo = form.cleaned_data["mobileNo"]
            resiNo = form.cleaned_data["resiNo"]
            edu_qualification = form.cleaned_data["edu_qualification"]
            prof_qualification = form.cleaned_data["prof_qualification"]
            other_qualification = form.cleaned_data["other_qualification"]
            position = form.cleaned_data["position"]
            if position == "Lecturer" or position == "Instructor":
                user_type = 4
            elif position == "Examiner":
                user_type = 5
            elif position == "Principal":
                user_type = 6
            else:
                user_type = 2

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      last_name=last_name, first_name=first_name, user_type=user_type,
                                                      profile_img=profile_img)
                print("User object created. Username:", username)
                print("User object:", user)
                user.staff.middle_name = middle_name
                user.staff.dob = dob
                user.staff.adrz = adrz
                user.staff.gender = gender
                user.staff.nic = nic
                user.staff.sf_idNo = sf_idNo
                user.staff.nationality = nationality
                user.staff.civil_status = civil_status
                user.staff.mobileNo = mobileNo
                user.staff.resiNo = resiNo
                user.staff.edu_qualification = edu_qualification
                user.staff.prof_qualification = prof_qualification
                user.staff.other_qualification = other_qualification
                user.staff.position = position
                user.save()

                messages.success(request, "Successfully Added")
                return HttpResponseRedirect(reverse("add_staff"))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Add")
                return HttpResponseRedirect(reverse("add_staff"))
        else:
            form = AddStaffForm(request.POST)
            return render(request, "admin_templates/add_staff.html", {"form": form})


def manage_staff(request):
    staff = Staff.objects.all()
    return render(request, "admin_templates/manage_staff.html", {"staff": staff})


def edit_staff(request, sf_id):
    request.session['sf_id'] = sf_id
    staff = Staff.objects.get(sf_id=sf_id)
    form = EditStaffForm()
    print("Profile Image URL:", staff.admin.profile_img.url)
    form.fields['profile_img'].initial = staff.admin.profile_img.url

    form.fields['first_name'].initial = staff.admin.first_name
    form.fields['middle_name'].initial = staff.middle_name
    form.fields['last_name'].initial = staff.admin.last_name
    form.fields['username'].initial = staff.admin.username
    form.fields['email'].initial = staff.admin.email
    form.fields['dob'].initial = staff.dob
    form.fields['adrz'].initial = staff.adrz
    form.fields['gender'].initial = staff.gender
    form.fields['nic'].initial = staff.nic
    form.fields['sf_idNo'].initial = staff.sf_idNo
    form.fields['nationality'].initial = staff.nationality
    form.fields['civil_status'].initial = staff.civil_status
    form.fields['mobileNo'].initial = staff.mobileNo
    form.fields['resiNo'].initial = staff.resiNo
    form.fields['edu_qualification'].initial = staff.edu_qualification
    form.fields['prof_qualification'].initial = staff.prof_qualification
    form.fields['other_qualification'].initial = staff.other_qualification
    form.fields['position'].initial = staff.position

    return render(request, "admin_templates/edit_staff.html",
                  {"form": form, "sf_id": sf_id, "username": staff.admin.username,
                   "user_profile_img": staff.admin.profile_img.url})


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        sf_id = request.session.get("sf_id")
        if sf_id == None:
            return HttpResponseRedirect(reverse("manage_staff"))
        form = EditStaffForm(request.POST, request.FILES)
        if form.is_valid():
            profile_img = form.cleaned_data["profile_img"]
            first_name = form.cleaned_data["first_name"]
            middle_name = form.cleaned_data["middle_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            dob = form.cleaned_data["dob"]
            adrz = form.cleaned_data["adrz"]
            gender = form.cleaned_data["gender"]
            nic = form.cleaned_data["nic"]
            sf_idNo = form.cleaned_data["sf_idNo"]
            nationality = form.cleaned_data["nationality"]
            civil_status = form.cleaned_data["civil_status"]
            mobileNo = form.cleaned_data["mobileNo"]
            resiNo = form.cleaned_data["resiNo"]
            edu_qualification = form.cleaned_data["edu_qualification"]
            prof_qualification = form.cleaned_data["prof_qualification"]
            other_qualification = form.cleaned_data["other_qualification"]
            position = form.cleaned_data["position"]
            if position == "Lecturer" or position == "Instructor":
                user_type = 4
            elif position == "Examiner":
                user_type = 5
            elif position == "Principal":
                user_type = 6
            else:
                user_type = 2

            try:

                staff = Staff.objects.get(sf_id=sf_id)
                staff.middle_name = middle_name
                staff.dob = dob
                staff.adrz = adrz
                staff.gender = gender
                staff.nic = nic
                staff.sf_idNo = sf_idNo
                staff.nationality = nationality
                staff.civil_status = civil_status
                staff.mobileNo = mobileNo
                staff.resiNo = resiNo
                staff.edu_qualification = edu_qualification
                staff.prof_qualification = prof_qualification
                staff.other_qualification = other_qualification
                staff.position = position

                user = CustomUser.objects.get(id=staff.admin.id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.user_type = user_type
                user.profile_img = profile_img
                user.save()
                staff.save()
                del request.session['sf_id']
                messages.success(request, "Successfully Updated")
                return HttpResponseRedirect(reverse("edit_staff", kwargs={"sf_id": sf_id}))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Update")
                return HttpResponseRedirect(reverse("edit_staff", kwargs={"sf_id": sf_id}))
        else:
            form = EditStaffForm(request.POST)
            staff = Staff.objects(sf_id=sf_id)
            return render(request, "admin_templates/edit_staff.html",
                          {"form": form, "sf_id": sf_id, "username": staff.admin.username})


def add_session(request):
    return render(request, "admin_templates/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("add_session"))
    else:
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")

        try:
            sessionyr = SessionYr(session_start=session_start, session_end=session_end)
            sessionyr.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("add_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("add_session"))


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def student_feedback_msg(request):
    feedbacks = FeedBackS.objects.all()
    return render(request, "admin_templates/student_fb.html", {"feedbacks": feedbacks})


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "admin_templates/admin_profile.html", {"user": user})


def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
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
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))


@csrf_exempt
def student_feedback_msg_replied(request):
    fb_id = request.POST.get("fb_id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackS.objects.get(fb_id=fb_id)
        feedback.fb_rpy = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@csrf_exempt
def mark_notification_as_read(request):
    notifications = NotificationSf.objects.filter(sf_id=request.user.id, is_read=False)
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return JsonResponse({'success': True})

def fetch_notifications(request):
    notifications = NotificationSf.objects.filter(sf_id=request.user.id)[:5]  # Get latest 5 notifications
    notification_html = ""
    for notification in notifications:
        notification_html += f"<a class='dropdown-item' href='/feedback/{notification.pk}'>{notification.notify_sf}</a>"
    data = {
        'count': NotificationSf.objects.filter(sf_id=request.user.id, is_read=False).count(),  # Count only unread notifications
        'html': notification_html,
    }
    return JsonResponse(data)

def staff_feedback_msg(request):
    feedbacks = FeedbackSf.objects.all()
    return render(request, "admin_templates/staff_fb.html", {"feedbacks": feedbacks})


@csrf_exempt
def staff_feedback_msg_replied(request):
    fbs_id = request.POST.get("fbs_id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedbackSf.objects.get(fbs_id=fbs_id)
        feedback.fbs_rpy = feedback_message
        feedback.save()

        # Create a new notification for the administrator
        notification = NotificationSf.objects.create(
            notify_sf=f"New reply to feedback message with ID: {fbs_id}",
            sf_id=feedback.sf_id,
            created_at=timezone.now()
        )

        return HttpResponse("True")
    except:
        return HttpResponse("False")





def student_leave_view(request):
    leaves = LeaveReportS.objects.all()
    return render(request, "admin_templates/student_leave_view.html", {"leaves": leaves})


def student_approve_leave(request, lr_id):
    leave = LeaveReportS.objects.get(lr_id=lr_id)
    leave.lr_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def student_disapprove_leave(request, lr_id):
    leave = LeaveReportS.objects.get(lr_id=lr_id)
    leave.lr_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_leave_view(request):
    leaves = LeaveReportSf.objects.all()
    return render(request, "admin_templates/staff_leave_view.html", {"leaves": leaves})


def admin_view_attendance(request):
    subjects = Subject.objects.all()
    yr_id = SessionYr.object.all()
    return render(request, "admin_templates/admin_view_attendance.html", {"subjects": subjects, "yr_id": yr_id})


@csrf_exempt
def admin_get_attendance_dates(request):
    subject = request.POST.get("subject")
    yr_id = request.POST.get("yr_id")
    subject_obj = Subject.objects.get(sub_id=subject)
    session_year_obj = SessionYr.object.get(yr_id=yr_id)
    attendance = Attendance.objects.filter(sub_id=subject_obj, yr_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"at_id": attendance_single.at_id, "at_date": str(attendance_single.at_date),
                "yr_id": attendance_single.yr_id.yr_id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    at_date = request.POST.get("at_date")
    attendance = Attendance.objects.get(at_id=at_date)

    # attendance_data=Attendance.objects.filter(at_id=attendance)
    list_data = []

    for student in attendance:
        data_small = {"id": student.st_id.admin.id,
                      "name": student.st_id.admin.first_name + " " + student.st_id.admin.last_name,
                      "status": student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def get_course_code(request):
    course_code = list(Trade.objects.values_list('c_id', 'c_code'))
    return JsonResponse({'course_code': course_code})


def add_batch(request):
    form = AddBatchForm()
    return render(request, "admin_templates/add_batch.html", {"form": form})


def add_batch_save(request):
    if request.method == "POST":
        form = AddBatchForm(request.POST)
        if form.is_valid():
            b_year = form.cleaned_data["b_year"]
            c_id = form.cleaned_data["course"]
            b_no = form.cleaned_data["b_no"]
            sem_no = form.cleaned_data["sem_no"]
            c_id = form.cleaned_data["course_n"]

            # Fetch c_code based on c_id
            try:
                course = Course.objects.get(pk=c_id)
                c_code = course.c_code
            except Course.DoesNotExist:
                messages.error(request, "Course not found.")
                return HttpResponseRedirect(reverse("add_batch"))

            # Format b_code with spaces
            b_code = f"{b_year} {c_code} {b_no}"

            try:
                batch = Batch(b_code=b_code, sem_no=sem_no)
                course_object = Course.objects.get(c_id=c_id)
                batch.c_id = course_object
                batch.save()
                # # Send a WebSocket message to update connected clients
                # channel_layer = get_channel_layer()
                # async_to_sync(channel_layer.group_send)(
                #     "batch_updates_group",
                #     {"type": "batch_update", "message": "New batch added"},
                # )
                messages.success(request, "Successfully Added Batch")
                return HttpResponseRedirect(reverse("add_batch"))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Add Batch")
        else:
            # If the form is not valid, display the error messages
            messages.error(request, "Failed To Add Batch. Please check the form errors.")

    # If the method is not POST or if there are errors, return to the form page with the existing form data
    form = AddBatchForm(request.POST)
    return render(request, "admin_templates/add_batch.html", {"form": form})


def manage_batch(request):
    search_batch = request.GET.get('search', '')
    if search_batch:
        batch = Batch.objects.filter(
            Q(b_code__icontains=search_batch) |
            Q(sem_no__icontains=search_batch)
        )
    else:
        batch = Batch.objects.all()
    return render(request, "admin_templates/manage_batch.html", {"batch": batch})


def edit_batch(request, b_id):
    request.session['b_id'] = b_id
    batch = Batch.objects.get(b_id=b_id)
    form = EditBatchForm()
    form.fields['b_code'].initial = batch.b_code
    form.fields['sem_no'].initial = batch.sem_no
    form.fields['course'].initial = batch.c_id_id
    return render(request, "admin_templates/edit_batch.html", {"form": form, "b_id": b_id})


def edit_batch_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        b_id = request.session.get("b_id")
        if b_id == None:
            return HttpResponseRedirect(reverse("manage_batch"))
        form = EditBatchForm(request.POST)
        if form.is_valid():
            b_code = form.cleaned_data["b_code"]
            sem_no = form.cleaned_data["sem_no"]
            c_id = form.cleaned_data["course"]
            try:
                batch = Batch(b_id=b_id)
                batch.b_code = b_code
                batch.sem_no = sem_no
                course_object = Course.objects.get(c_id=c_id)
                batch.c_id = course_object
                batch.save()
                messages.success(request, "Successfully Updated")
                return HttpResponseRedirect(reverse("edit_batch", kwargs={"b_id": b_id}))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Update batch")
                return HttpResponseRedirect(reverse("edit_batch", kwargs={"b_id": b_id}))
        else:
            form = EditBatchForm(request.POST)
            return render(request, "admin_templates/edit_batch.html", {"form": form, "b_id": b_id})


def ws_connect(event):
    pass


def ws_disconnect(event):
    pass


def ws_receive(event):
    pass


@csrf_exempt
def check_modulename_exist(request):
    mod_name = request.POST.get("mod_name", "").strip()  # Remove leading/trailing whitespaces
    if mod_name:
        # Check if a similar trade name exists (case-insensitive and ignoring spaces)
        module_exists = Module.objects.filter(
            Q(mod_name__icontains=mod_name) | Q(mod_name__icontains=mod_name.replace(" ", ""))
        ).exists()
        return JsonResponse({'exists': module_exists})  # Return the result as JSON
    else:
        return JsonResponse({'exists': False})


def get_sub(request):
    c_id = request.GET.get('c_id')
    try:
        # Find the Course instance based on the provided course id
        course = Course.objects.get(c_id=c_id)
        # Retrieve subjects for the given course
        subjects = Subject.objects.filter(c_id=course).values('sub_id', 'sub_name')

        return JsonResponse({'subjects': list(subjects)})
    except Course.DoesNotExist:
        return JsonResponse({'subjects': []})


def add_module(request):
    form = AddModuleForm()
    return render(request, "admin_templates/add_module.html", {"form": form})


def add_module_save(request):
    if request.method == "POST":
        form = AddModuleForm(request.POST)
        if form.is_valid():
            mod_code = form.cleaned_data["mod_code"]
            mod_name = form.cleaned_data["mod_name"]
            duration_hours = form.cleaned_data["duration_hours"]
            academic_weeks = form.cleaned_data["academic_weeks"]
            c_id = form.cleaned_data["course"]
            sub_id = form.cleaned_data["subject"]
            try:
                module = Module(
                    mod_code=mod_code,
                    mod_name=mod_name,
                    duration_hours=duration_hours,
                    academic_weeks=academic_weeks
                )
                course_object = Course.objects.get(c_id=c_id)
                module.c_id = course_object
                # Ensure that the selected subject is related to the chosen course
                subject_object = Subject.objects.get(sub_id=sub_id, c_id=course_object)
                module.sub_id = subject_object
                module.save()
                messages.success(request, "Successfully Added ")
                return HttpResponseRedirect(reverse("add_module"))
            except Subject.DoesNotExist:
                messages.error(request, "The selected subject is not related to the chosen course.")
            except ValidationError as e:
                messages.error(request, e.message_dict)
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Add Module")
        else:
            print(form.errors)
            messages.error(request, "Form is not valid")
    else:
        form = AddModuleForm()
    return render(request, "admin_templates/add_module.html", {"form": form})


def manage_module(request):
    search_query = request.GET.get('search', '')
    modules = Module.objects.all().order_by('mod_id')

    if search_query:
        modules = modules.filter(
            Q(mod_name__icontains=search_query) |
            Q(mod_code__icontains=search_query) |
            Q(duration_hours__icontains=search_query) |
            Q(academic_weeks__icontains=search_query) |
            Q(created_at__icontains=search_query)
        )

    paginator = Paginator(modules, 8)
    page_number = request.GET.get('page', 1)

    try:
        modules = paginator.page(page_number)
    except EmptyPage:
        modules = paginator.page(paginator.num_pages)

    return render(request, "admin_templates/manage_module.html", {"modules": modules, "search_query": search_query})


def mod_pdf(request, search_query=None):
    try:
        if search_query is None:
            search_query = request.GET.get('search', '')

        # Retrieve selected checkboxes IDs
        selected_ids = request.GET.get('selected_ids', '').split(',')
        # Remove empty strings from selected_ids list
        selected_ids = [id for id in selected_ids if id]

        # Initialize response
        response = HttpResponse(content_type='application/pdf')

        buffer = BytesIO()
        p = SimpleDocTemplate(buffer, pagesize=letter)

        table_data = [['ID', 'Module Name', 'Module Code', 'Duration', 'Academic Weeks']]

        # Fetch modules based on the search query
        modules = Module.objects.filter(
            Q(mod_name__icontains=search_query) |
            Q(mod_code__icontains=search_query) |
            Q(duration_hours__icontains=search_query) |
            Q(academic_weeks__icontains=search_query)
        ).order_by('mod_id')

        # If selected IDs are provided, export only selected data
        if selected_ids:
            modules = modules.filter(mod_id__in=selected_ids)

        # Add unselected modules matching the search query to the table data
        for module in modules:
            if module.mod_id not in selected_ids:  # Check if the module is not selected
                table_data.append(
                    [module.mod_id, module.mod_name, module.mod_code, module.duration_hours, module.academic_weeks])

        # Define table style and build PDF
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Create table and elements for PDF
        table = Table(table_data)
        table.setStyle(style)
        elements = [table]

        # Build PDF and write to response
        p.build(elements)
        pdf = buffer.getvalue()
        buffer.close()

        # Set the PDF content in the response
        response.write(pdf)

        # Set the content-disposition header to inline
        response['Content-Disposition'] = 'inline; filename="module_data.pdf"'

    except Exception as e:
        # Handle other exceptions
        response = HttpResponse(f"An error occurred: {str(e)}")

    return response


def mod_csv():
    return None


def edit_module(request, mod_id):
    request.session['mod_id'] = mod_id
    module = Module.objects.get(mod_id=mod_id)
    form = EditModuleForm()
    form.fields['mod_name'].initial = module.mod_name
    form.fields['mod_code'].initial = module.mod_code
    form.fields['duration_hours'].initial = module.duration_hours
    form.fields['academic_weeks'].initial = module.academic_weeks
    form.fields['course'].initial = module.c_id_id
    form.fields['subject'].initial = module.sub_id_id
    return render(request, "admin_templates/edit_module.html", {"form": form, "mod_id": mod_id})

def edit_module_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        mod_id = request.session.get("mod_id")
        if mod_id is None:
            return HttpResponseRedirect(reverse("manage_module"))
        form = EditModuleForm(request.POST)
        if form.is_valid():
            mod_code = form.cleaned_data["mod_code"]
            mod_name = form.cleaned_data["mod_name"]
            duration_hours = form.cleaned_data["duration_hours"]
            academic_weeks = form.cleaned_data["academic_weeks"]
            c_id = form.cleaned_data["course"]
            sub_id = form.cleaned_data["subject"]
            try:
                module = Module.objects.get(mod_id=mod_id)
                module.mod_code = mod_code
                module.mod_name = mod_name
                module.duration_hours = duration_hours
                module.academic_weeks = academic_weeks
                module.c_id_id = c_id
                module.sub_id_id = sub_id
                module.save()
                messages.success(request, "Successfully Updated")
                return HttpResponseRedirect(reverse("edit_module", args=[mod_id]))
            except Exception as e:
                print(e)
                messages.error(request, "Failed To Update Module")
                return HttpResponseRedirect(reverse("edit_module", args=[mod_id]))
        else:
            return render(request, "admin_templates/edit_module.html", {"form": form})



logger = logging.getLogger(__name__)


def coz_payment(request):
    search_query = request.GET.get('search', '')
    user = request.user

    if user.user_type == '1':  # Check if the user is an administrator
        payments = Payment.objects.all().order_by('pay_id')
    else:
        try:
            # Retrieve the associated Student instance
            student = Student.objects.get(admin=user)
            payments = Payment.objects.filter(st_id=student).order_by('pay_id')
        except Student.DoesNotExist:
            # If the user is not a student, return a forbidden response or handle appropriately
            return HttpResponseForbidden("You are not authorized to view this page.")

    if search_query:
        payments = payments.filter(
            Q(st_id__st_idNo__icontains=search_query) |
            Q(c_id__c_name__icontains=search_query) |
            Q(b_id__b_code__icontains=search_query) |
            Q(price__icontains=search_query) |
            Q(payment_date__icontains=search_query)
        )

    paginator = Paginator(payments, 8)
    page_number = request.GET.get('page', 1)

    try:
        payments = paginator.page(page_number)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)

    return render(request, "admin_templates/course_payment_view.html",
                  {"payments": payments, "search_query": search_query})



def coz_pay_pdf(request, search_query=None):
    try:
        if search_query is None:
            search_query = request.GET.get('search', '')

        # Retrieve selected checkboxes IDs
        selected_ids = request.GET.get('selected_ids', '').split(',')
        # Remove empty strings from selected_ids list
        selected_ids = [id for id in selected_ids if id]

        # Fetch payments based on user type and search query
        user = request.user
        if user.user_type == '1':  # Administrator
            payments = Payment.objects.all()
        else:
            try:
                student = Student.objects.get(admin=user)
                payments = Payment.objects.filter(st_id=student)
            except Student.DoesNotExist:
                logger.warning(f"No Student record found for user {user.id}")
                return HttpResponseForbidden("You are not authorized to view this page.")

        # If a search query exists, filter by it
        if search_query:
            payments = payments.filter(
                Q(st_id__st_idNo__icontains=search_query) |
                Q(c_id__c_code__icontains=search_query) |
                Q(b_id__b_code__icontains=search_query) |
                Q(price__icontains=search_query) |
                Q(payment_date__icontains=search_query)
            )

        # If selected IDs are provided, filter by them
        if selected_ids:
            payments = payments.filter(pay_id__in=selected_ids)

        # Initialize response
        response = HttpResponse(content_type='application/pdf')

        # Initialize PDF buffer
        buffer = BytesIO()

        # Create PDF document
        p = SimpleDocTemplate(buffer, pagesize=letter)

        # Define elements for PDF
        elements = []

        # Adding headers and footers
        class HeaderFooterTemplate(PageTemplate):
            def __init__(self, id=None, **kwargs):
                super().__init__(id=id, frames=[Frame(1 * cm, 2 * cm, 17 * cm, 24 * cm)])

            def beforeDrawPage(self, canvas, doc):
                canvas.saveState()

                # Draw the image in the top left corner
                img_path1 = 'static/dist/img/sl_gov.png'
                img1 = ImageReader(img_path1)
                canvas.drawImage(img1, 1 * inch, letter[1] - 1 * inch, width=60, height=60, mask='auto')

                # Draw the second image under the first image
                img_path2 = 'static/dist/img/touch-icon.png'
                img2 = ImageReader(img_path2)
                canvas.drawImage(img2, 1 * inch, letter[1] - 1.9 * inch, width=60, height=60, mask='auto')

                # Draw the third image in the top right corner
                img_path3 = 'static/dist/img/mis.png'
                img3 = ImageReader(img_path3)
                canvas.drawImage(img3, letter[0] - 1.5 * inch, letter[1] - 1 * inch, width=60, height=60, mask='auto')

                canvas.setFont('Helvetica-Bold', 20)
                canvas.setFillColor(colors.purple)
                canvas.drawString((letter[0] - 280) / 2, letter[1] - 0.5 * inch, "Technical College - Gampaha")

                pay_info = f"Student Payment Data"
                canvas.setFont('Helvetica-Bold', 16)
                canvas.drawString((letter[0] - 200) / 2, letter[1] - 0.9 * inch, pay_info)

                canvas.setFont('Helvetica-Bold', 12)
                canvas.setFillColor(colors.black)

                # Draw horizontal line
                canvas.setLineWidth(2)
                canvas.setStrokeColor(colors.darkblue)
                canvas.line(1 * inch, letter[1] - 2.25 * inch, letter[0] - 1 * inch, letter[1] - 2.25 * inch)

                canvas.restoreState()

        p.addPageTemplates([HeaderFooterTemplate()])

        # Define table data
        table_data = [['ID', 'Student ID', 'Course', 'Batch', 'Price', 'Payment Date']]
        for payment in payments:
            table_data.append([str(payment.pay_id), str(payment.st_id.st_idNo), str(payment.c_id.c_code), str(payment.b_id.b_code), str(payment.price), str(payment.payment_date)])  # Convert to strings

        # Define column widths for the table
        column_widths = [30, 60, 50, 90, 50, 200]

        # Define styles for table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), (1, 1, 1)),
            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
            ('TEXTCOLOR', (0, 0), (-1, -1), (0, 0, 0)),  # Text color
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment
            ('INNERGRID', (0, 0), (-1, -1), 0.25, (0, 0, 0)),  # Inner grid line style
            ('WORDWRAP', (0, 0), (-1, -1)),  # Enable word wrap
        ])

        # Create table and add it to the elements
        table = Table(table_data, colWidths=column_widths)
        table.setStyle(style)
        elements.append(Spacer(1, 1.9 * inch))  # Add spacer before the table
        elements.append(table)  # Add table below the horizontal line

        # Build the PDF document
        p.build(elements)

        # Close the buffer
        buffer.seek(0)
        response.write(buffer.getvalue())
        buffer.close()

        # Set the content-disposition header to inline
        response['Content-Disposition'] = 'inline; filename="course_payment_report.pdf"'

        return response

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        response = HttpResponse(f"An error occurred: {str(e)}")
        return response



def coz_pay_csv(request, search_query=None):
    try:
        if search_query is None:
            search_query = request.GET.get('search', '')

        # Retrieve selected checkbox IDs
        selected_ids = request.GET.get('selected_ids', '').split(',')
        # Remove empty strings from selected_ids list
        selected_ids = [id for id in selected_ids if id]

        # Fetch payments based on user type and search query
        user = request.user
        if user.user_type == '1':  # Administrator
            payments = Payment.objects.all()
        else:
            try:
                student = Student.objects.get(admin=user)
                payments = Payment.objects.filter(st_id=student)
            except Student.DoesNotExist:
                logger.warning(f"No Student record found for user {user.id}")
                return HttpResponseForbidden("You are not authorized to view this page.")

        if search_query:
            payments = payments.filter(
                Q(st_id__st_idNo__icontains=search_query) |
                Q(c_id__c_name__icontains=search_query) |
                Q(b_id__b_code__icontains=search_query) |
                Q(price__icontains=search_query) |
                Q(payment_date__icontains=search_query)
            )

        if selected_ids:
            payments = payments.filter(pay_id__in=selected_ids)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="course_payment_sheet.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Student ID', 'Course', 'Batch', 'Price', 'Payment Date'])

        for payment in payments:
            writer.writerow([payment.pay_id, payment.st_id.st_idNo, payment.c_id.c_name, payment.b_id.b_code, payment.price, payment.payment_date])

        return response

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        response = HttpResponse(f"An error occurred: {str(e)}")
        return response


