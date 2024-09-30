import csv
import datetime
import logging
from io import BytesIO

import stripe
import vonage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageTemplate, Spacer, Flowable, Frame
from reportlab.lib.units import inch
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus.frames import Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from twilio.rest import Client
from django.core.mail import send_mail
from misweb.utils import send_sms_via_twilio
from mistech.form import PaymentForm
from mistech.models import Student, Course, Subject, CustomUser, Attendance, LeaveReportS, FeedBackS, Payment, Batch
from django.shortcuts import get_object_or_404

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.db.models import Count, F, FloatField, ExpressionWrapper


def student_home(request):
    student_obj = Student.objects.get(admin=request.user)
    attendance_total = Attendance.objects.filter(st_id=student_obj).count()
    attendance_present = Attendance.objects.filter(st_id=student_obj, status="Present").count()
    attendance_absent = Attendance.objects.filter(st_id=student_obj, status="Absent").count()
    course = Course.objects.get(c_id=student_obj.c_id_id)
    subjects = Subject.objects.filter(c_id=course).count()

    subject_name = []
    data_present = []
    data_absent = []
    attendance_percentage = []

    subject_data = Subject.objects.filter(c_id=student_obj.c_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(sub_id=subject.sub_id)
        attendance_present_count = Attendance.objects.filter(at_id__in=attendance, status="Present",
                                                             st_id=student_obj.st_id).count()
        attendance_absent_count = Attendance.objects.filter(at_id__in=attendance, status="Absent",
                                                            st_id=student_obj.st_id).count()
        subject_name.append(subject.sub_code)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

        # Calculate attendance percentage
        total_attendance = attendance_present_count + attendance_absent_count
        if total_attendance > 0:
            percentage = (attendance_present_count / total_attendance) * 100
        else:
            percentage = 0
        attendance_percentage.append(round(percentage, 2))

    return render(request, "student_templates/student_home_content.html",
                  {"total_attendance": attendance_total, "attendance_absent": attendance_absent,
                   "attendance_present": attendance_present, "subjects": subjects, "data_name": subject_name,
                   "data1": data_present, "data2": data_absent, "attendance_percentage": attendance_percentage})


def get_stcourse(request):
    try:
        # Get the logged-in student
        student = Student.objects.get(admin=request.user)

        # Fetch the course associated with the student
        course = student.c_id  # Assuming c_id is the foreign key field in the Student model

        # Prepare the course details for JSON response
        if course:
            course_details = {
                'id': course.c_id,
                'c_name': course.c_name,
                'c_code': course.c_code
            }
            # Print the fetched course for debugging
            # print("Course:", course_details)
            return JsonResponse({'course': course_details})
        else:
            print("No course found for the student.")  # Add a print statement for no course found
            return JsonResponse({'course': None})
    except Student.DoesNotExist:
        print("No student found.")  # Add a print statement for no student found
        return JsonResponse({'course': None})
    except Course.DoesNotExist:
        print("No course found.")  # Add a print statement for no course found
        return JsonResponse({'course': None})


def get_stbatch(request):
    try:
        # Get the logged-in student
        student = Student.objects.get(admin=request.user)

        # Fetch the batch associated with the student
        batch = student.b_id

        # Prepare the batch details for JSON response
        if batch:
            batch_details = {
                'id': batch.b_id,
                'b_code': batch.b_code
            }
            # Return batch details as JSON response
            return JsonResponse({'batch': batch_details})
        else:
            print("No batch found for the student.")
            return JsonResponse({'batch': None})
    except Student.DoesNotExist:
        print("No student found.")
        return JsonResponse({'batch': None})


@login_required
def make_payment(request):
    if request.method == 'POST':
        try:
            token = request.POST.get('stripeToken')
            cvc = request.POST.get('cvc')
            amount = request.POST.get('amount')
            course_name = request.POST.get('course_name')  # Retrieve the course name from the form
            batch_code = request.POST.get('batch_code')  # Retrieve the batch code from the form

            amount_in_rupees = float(amount)
            if amount_in_rupees < 0.50:
                amount_in_rupees = 0.50

            stripe.api_key = settings.STRIPE_SECRET_KEY
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount_in_rupees * 100),
                currency='inr',
                payment_method_types=['card'],
                payment_method_data={
                    'type': 'card',  # Specify the type of payment method
                    'card': {
                        'token': token,  # Use the token provided by Stripe
                    }
                },
                confirm=True,
                description='Course Payment',
            )
            send_email(request.user.email)
            # send_sms_via_twilio(request.user.student.mobileNo, "Payment successful!")


            save_payment(request.user.student, course_name, batch_code,
                         amount_in_rupees)  # Pass the retrieved batch code

            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            return JsonResponse({'error': str(e)})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        student = request.user.student
        course_name = student.c_id.c_name
        batch_code = student.b_id.b_code
        mobile_number = student.mobileNo
        email = request.user.email
        context = {
            'mobile_number': mobile_number,
            'email': email,
            'course_name': course_name,
            'batch_code': batch_code,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        }

    return render(request, 'student_templates/payment_form.html', context=context)


def send_email(email):
    # Email
    send_mail(
        'Payment Successful',
        'Your payment was successful.',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def save_payment(student, course_name, batch_code, amount):
    try:
        # Attempt to find the course by case-insensitive search
        course = Course.objects.filter(Q(c_name__iexact=course_name) | Q(c_code__iexact=course_name)).first()

        if course is None:
            # If no course is found, raise an exception
            raise Course.DoesNotExist("Course with name '{}' does not exist.".format(course_name))

        # Retrieve the batch instance by batch code
        batch = Batch.objects.get(b_code=batch_code)

        payment = Payment.objects.create(
            st_id=student,
            c_id=course,
            b_id=batch,  # Assign the Batch instance
            price=amount,
        )
        payment.save()
    except Course.DoesNotExist:
        # Handle the case where the course name does not exist
        raise ValueError("Course with name '{}' does not exist.".format(course_name))
    except Batch.DoesNotExist:
        # Handle the case where the batch code does not exist
        raise ValueError("Batch with code '{}' does not exist.".format(batch_code))


# def send_sms(mobile_number, message):
#     # Twilio SMS
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     message = client.messages.create(
#         body=message,
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=mobile_number
#     )


def st_view_attendance(request):
    search_query = request.GET.get('search', '')
    user = request.user

    # Retrieve the corresponding Student instance
    student = get_object_or_404(Student, admin=user)

    # Filter Attendance objects based on the Student instance
    attendances = Attendance.objects.filter(st_id=student).order_by('at_id')

    if search_query:
        attendances = attendances.filter(
            Q(at_date__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    paginator = Paginator(attendances, 8)
    page_number = request.GET.get('page', 1)

    try:
        attendances = paginator.page(page_number)
    except EmptyPage:
        attendances = paginator.page(paginator.num_pages)

    return render(request, "student_templates/student_view_attendance.html",
                  {"attendances": attendances, "search_query": search_query})


def st_at_pdf(request, search_query=None):
    try:
        if search_query is None:
            search_query = request.GET.get('search', '')

        # Retrieve selected checkboxes IDs
        selected_ids = request.GET.get('selected_ids', '').split(',')
        # Remove empty strings from selected_ids list
        selected_ids = [id for id in selected_ids if id]

        # Fetch modules based on the search query
        attendances = Attendance.objects.all()

        # If a search query exists, filter by it
        if search_query:
            attendances = attendances.filter(
                Q(at_date__icontains=search_query) |
                Q(status__icontains=search_query)
            )

        # If no selected IDs and no search query, filter by logged-in student
        if not selected_ids and not search_query:
            # Assuming the logged-in user is a student
            student = Student.objects.get(admin=request.user)
            attendances = attendances.filter(st_id=student)

        # If selected IDs are provided, export only selected data
        if selected_ids:
            attendances = attendances.filter(at_id__in=selected_ids)

        # Initialize response
        response = HttpResponse(content_type='application/pdf')

        # Initialize PDF buffer
        buffer = BytesIO()

        # Create PDF document
        p = SimpleDocTemplate(buffer, pagesize=letter)

        # Define elements for PDF
        elements = []
        # Fetch user, course, and batch information
        user = request.user  # Assuming request.user contains the user object
        student = Student.objects.get(admin=user)
        course = student.c_id
        batch = student.b_id

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

                at_info = f"Student Attendance Data"
                canvas.setFont('Helvetica-Bold', 16)
                canvas.drawString((letter[0] - 200) / 2, letter[1] - 0.9 * inch, at_info)

                canvas.setFont('Helvetica-Bold', 12)
                canvas.setFillColor(colors.black)

                # Course name
                course_info = f"Course: {course.c_name}"
                text_width = canvas.stringWidth(course_info, "Helvetica-Bold", 12)
                canvas.drawString((letter[0] - text_width) / 2, letter[1] - 1.25 * inch, course_info)

                # Batch code
                batch_info = f"Batch Code: {batch.b_code}"
                text_width = canvas.stringWidth(batch_info, "Helvetica-Bold", 12)
                canvas.drawString((letter[0] - text_width) / 2, letter[1] - 1.5 * inch, batch_info)

                # User's full name
                user_full_name = f"Student: {user.first_name} {user.last_name}"
                text_width = canvas.stringWidth(user_full_name, "Helvetica-Bold", 12)
                canvas.drawString((letter[0] - text_width) / 2, letter[1] - 1.75 * inch, user_full_name)

                # Student ID number
                student_id = f"Student ID: {student.st_idNo}"
                text_width = canvas.stringWidth(student_id, "Helvetica-Bold", 12)
                canvas.drawString((letter[0] - text_width) / 2, letter[1] - 2 * inch, student_id)

                # Draw horizontal line
                canvas.setLineWidth(2)
                canvas.setStrokeColor(colors.darkblue)
                canvas.line(1 * inch, letter[1] - 2.25 * inch, letter[0] - 1 * inch, letter[1] - 2.25 * inch)

                canvas.restoreState()

        p.addPageTemplates([HeaderFooterTemplate()])

        # Define table data
        table_data = [['ID', 'Date', 'Status']]
        for attendance in attendances:
            table_data.append([str(attendance.at_id), str(attendance.at_date), attendance.status])  # Convert to strings

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
        table = Table(table_data)
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
        response['Content-Disposition'] = 'inline; filename="personal_student_attendance.pdf"'

        return response

    except Exception as e:
        # Handle other exceptions
        response = HttpResponse(f"An error occurred: {str(e)}")
        return response


def st_at_csv(request, search_query=None):
    try:
        # Retrieve search query
        if search_query is None:
            search_query = request.GET.get('search', '')

        # Retrieve selected checkbox IDs
        selected_ids = request.GET.get('selected_ids', '').split(',')
        # Remove empty strings from selected_ids list
        selected_ids = [id for id in selected_ids if id]

        # Fetch modules based on the search query
        user = request.user
        student = Student.objects.get(admin=user)  # Assuming Student model has a ForeignKey to User model
        attendances = Attendance.objects.filter(st_id=student)

        # If a search query exists, filter by it
        if search_query:
            attendances = attendances.filter(
                Q(at_date__icontains=search_query) |
                Q(status__icontains=search_query)
            )

        # If selected IDs are provided, filter by them
        if selected_ids:
            attendances = attendances.filter(at_id__in=selected_ids)

        # Define CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="personal_student_attendance.csv"'

        # Write CSV data
        writer = csv.writer(response)
        writer.writerow(['ID', 'Date', 'Status'])  # Write header row

        # Write data rows for searched and selected attendances
        for attendance in attendances:
            writer.writerow([attendance.at_id, attendance.at_date, attendance.status])

        return response

    except Exception as e:
        # Handle other exceptions
        response = HttpResponse(f"An error occurred: {str(e)}")
        return response


def student_apply_leave(request):
    st_obj = Student.objects.get(admin=request.user.id)
    lv_data = LeaveReportS.objects.filter(st_id=st_obj)

    return render(request, "student_templates/student_apply_leave.html", {"lv_data": lv_data})


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


def student_feedback(request):
    st_obj = Student.objects.get(admin=request.user.id)
    feedback_data = FeedBackS.objects.filter(st_id=st_obj)

    return render(request, "student_templates/student_feedback.html", {"feedback_data": feedback_data})


def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        fb_msg = request.POST.get("fb_msg")

        st_obj = Student.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackS(st_id=st_obj, fb=fb_msg, fb_rpy="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "student_templates/student_profile.html", {"user": user})


def student_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))


@csrf_exempt
def student_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        student = Student.objects.get(admin=request.user.id)
        student.fcm_token = token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
