"""misweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from mistech import views, AdminViews, InstructorViews, StaffViews, StudentViews, ExaminerViews, PrincipalViews, PViews, \
    consumers
from misweb import settings

urlpatterns = [
    path('', views.showLoginPage, name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('admin/', admin.site.urls),
    path('reset/', include('django.contrib.auth.urls')),
    path('logout_user', views.LogoutUser, name="logout"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('admin_home', AdminViews.admin_home, name="admin_home"),

    path('get_course_code', AdminViews.get_course_code, name='get_course_code'),
    path('add_batch', AdminViews.add_batch, name="add_batch"),
    path('add_batch_save', AdminViews.add_batch_save, name="add_batch_save"),
    path('manage_batch', AdminViews.manage_batch, name="manage_batch"),
    path('manage_batch/export_all/', AdminViews.manage_batch, {'export_all': True}, name='export_all_batchs'),
    path('edit_batch/<str:b_id>', AdminViews.edit_batch, name="edit_batch"),
    path('edit_batch_save', AdminViews.edit_batch_save, name="edit_batch_save"),
    # Include the WebSocket URL pattern
    path('ws/localhost:3000/', consumers.MtechConsumer.as_asgi()),

    path('add_trade', AdminViews.add_trade, name="add_trade"),
    path('add_trade_save', AdminViews.add_trade_save, name="add_trade_save"),
    path('check_tradename_exist', AdminViews.check_tradename_exist, name="check_tradename_exist"),
    path('get_trade_names', AdminViews.get_trade_names, name='get_trade_names'),
    path('manage_trade', AdminViews.manage_trade, name="manage_trade"),
    path('tr_pdf/<str:search_tr>/', AdminViews.tr_pdf, name="tr_pdf"),
    path('tr_csv/<str:search_tr>/', AdminViews.tr_csv, name="tr_csv"),

    path('edit_trade/<str:tr_id>', AdminViews.edit_trade, name="edit_trade"),
    path('edit_trade_save', AdminViews.edit_trade_save, name="edit_trade_save"),

    path('add_course', AdminViews.add_course, name="add_course"),
    path('add_course_save', AdminViews.add_course_save, name="add_course_save"),

    path('manage_course', AdminViews.manage_course, name="manage_course"),
    path('manage_course/export_all/', AdminViews.manage_course, {'export_all': True}, name='export_all_courses'),
    path('c_pdf/', AdminViews.c_pdf, name='c_pdf'),
    path('c_pdf/<str:search_query>/', AdminViews.c_pdf, name='c_pdf_with_query'),
    path('edit_course/<str:c_id>', AdminViews.edit_course, name="edit_course"),
    path('edit_course_save', AdminViews.edit_course_save, name="edit_course_save"),
    path('c_csv/', AdminViews.c_csv, name="c_csv"),

    path('check_subjectname_exist', AdminViews.check_subjectname_exist, name="check_subjectname_exist"),
    path('get_course_names', AdminViews.get_course_names, name='get_course_names'),
    path('get_staff_idnos', AdminViews.get_staff_idnos, name='get_staff_idnos'),
    path('add_subject', AdminViews.add_subject, name="add_subject"),
    path('add_subject_save', AdminViews.add_subject_save, name="add_subject_save"),
    path('manage_subject', AdminViews.manage_subject, name="manage_subject"),
    path('get_staff_ids/<str:sub_id>', AdminViews.get_staff_ids, name="get_staff_ids"),
    path('edit_subject/<str:sub_id>', AdminViews.edit_subject, name="edit_subject"),
    path('edit_subject_save', AdminViews.edit_subject_save, name="edit_subject_save"),

    path('add_module', AdminViews.add_module, name="add_module"),
    path('add_module_save', AdminViews.add_module_save, name="add_module_save"),

    path('manage_module', AdminViews.manage_module, name="manage_module"),
    path('manage_module/export_all/', AdminViews.manage_module, {'export_all': True}, name='export_all_modules'),
    path('edit_module/<str:mod_id>', AdminViews.edit_module, name="edit_module"),
    path('edit_module_save', AdminViews.edit_module_save, name="edit_module_save"),
    path('mod_pdf/', AdminViews.mod_pdf, name='mod_pdf'),
    path('mod_pdf/<str:search_query>/', AdminViews.mod_pdf, name='mod_pdf_with_query'),
    path('mod_csv/', AdminViews.mod_csv, name="mod_csv"),

    path('get_sub', AdminViews.get_sub, name="get_sub"),
    path('check_modulename_exist', AdminViews.check_modulename_exist, name="check_modulename_exist"),

    path('add_student', AdminViews.add_student, name="add_student"),
    path('add_student_save', AdminViews.add_student_save, name="add_student_save"),
    path('manage_student', AdminViews.manage_student, name="manage_student"),
    path('edit_student/<str:st_id>', AdminViews.edit_student, name="edit_student"),
    path('edit_student_save', AdminViews.edit_student_save, name="edit_student_save"),
    path('add_staff', AdminViews.add_staff, name="add_staff"),
    path('add_staff_save', AdminViews.add_staff_save, name="add_staff_save"),
    path('manage_staff', AdminViews.manage_staff, name="manage_staff"),
    path('edit_staff/<str:sf_id>', AdminViews.edit_staff, name="edit_staff"),
    path('edit_staff_save', AdminViews.edit_staff_save, name="edit_staff_save"),
    path('add_session', AdminViews.add_session, name="add_session"),
    path('add_session_save', AdminViews.add_session_save, name="add_session_save"),
    path('student_feedback_msg', AdminViews.student_feedback_msg, name="student_feedback_msg"),
    path('student_feedback_msg_replied', AdminViews.student_feedback_msg_replied,
         name="student_feedback_msg_replied"),
    path('staff_feedback_msg', AdminViews.staff_feedback_msg, name="staff_feedback_msg"),
    path('staff_feedback_msg_replied', AdminViews.staff_feedback_msg_replied,
         name="staff_feedback_msg_replied"),
    path('student_leave_view', AdminViews.student_leave_view, name="student_leave_view"),
    path('staff_leave_view', AdminViews.staff_leave_view, name="staff_leave_view"),
    path('student_approve_leave/<str:lr_id>', AdminViews.student_approve_leave, name="student_approve_leave"),
    path('student_disapprove_leave/<str:lr_id>', AdminViews.student_disapprove_leave,
         name="student_disapprove_leave"),
    path('admin_view_attendance', AdminViews.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates', AdminViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student', AdminViews.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_profile', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_save', AdminViews.admin_profile_save, name="admin_profile_save"),

    path('check_email_exist', AdminViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist', AdminViews.check_username_exist, name="check_username_exist"),
    path('check_coursename_exist', AdminViews.check_coursename_exist, name="check_coursename_exist"),

    # Notification
    path('fetch_notifications/', AdminViews.fetch_notifications, name='fetch_notifications'),
    path('mark_notification_as_read', AdminViews.mark_notification_as_read,
         name="mark_notification_as_read"),


    #coz payment
    path('coz_payment', AdminViews.coz_payment, name="coz_payment"),

    path('coz_pay_pdf/', AdminViews.coz_pay_pdf, name='coz_pay_pdf'),
    path('coz_pay_pdf/<str:search_query>/', AdminViews.coz_pay_pdf, name='coz_pay_pdf_with_query'),

    path('coz_pay_csv/', AdminViews.coz_pay_csv, name="coz_pay_csv"),
    path('coz_pay_csv/<str:search_query>/', AdminViews.coz_pay_csv, name='coz_pay_csv_with_query'),


    # Staff URL Path
    path('staff_home', StaffViews.staff_home, name="staff_home"),

    # Instructor URL Path
    path('instructor_home', InstructorViews.instructor_home, name="instructor_home"),

    path('get_subject/', InstructorViews.get_subject, name='get_subject'),
    path('get_batches/', InstructorViews.get_batches, name='get_batches'),
    path('instructor_take_attendance', InstructorViews.instructor_take_attendance,
         name="instructor_take_attendance"),

    path('sf_view_attendance', InstructorViews.sf_view_attendance, name="sf_view_attendance"),

    path('sf_at_pdf/', InstructorViews.sf_at_pdf, name='sf_at_pdf'),
    path('sf_at_pdf/<str:search_query>/', InstructorViews.sf_at_pdf, name='sf_at_pdf_with_query'),

    path('sf_at_csv/', InstructorViews.sf_at_csv, name="sf_at_csv"),
    path('sf_at_csv/<str:search_query>/', InstructorViews.sf_at_csv, name='sf_at_csv_with_query'),

    path('instructor_apply_leave', InstructorViews.instructor_apply_leave, name="instructor_apply_leave"),
    path('instructor_apply_leave_save', InstructorViews.instructor_apply_leave_save,
         name="instructor_apply_leave_save"),
    path('instructor_feedback', InstructorViews.instructor_feedback, name="instructor_feedback"),
    path('instructor_feedback_save', InstructorViews.instructor_feedback_save, name="instructor_feedback_save"),
    path('instructor_profile', InstructorViews.instructor_profile, name="instructor_profile"),
    path('instructor_profile_save', InstructorViews.instructor_profile_save, name="instructor_profile_save"),

    path('instructor_task', InstructorViews.instructor_task, name="instructor_task"),
    path('instructor_task_save', InstructorViews.instructor_task_save, name="instructor_task_save"),

    path('manage_instructor_task', InstructorViews.manage_instructor_task,
         name="manage_instructor_task"),
    path('manage_instructor_task/export_all/', InstructorViews.manage_instructor_task,
         {'export_all': True}, name='export_all_tasks'),
    path('edit_instructor_task/<str:tk_id>', InstructorViews.edit_instructor_task,
         name="edit_instructor_task"),
    path('edit_instructor_task_save', InstructorViews.edit_instructor_task_save,
         name="edit_instructor_task_save"),
    path('task_pdf/', InstructorViews.task_pdf, name='task_pdf'),
    path('task_pdf/<str:search_query>/', InstructorViews.task_pdf, name='task_pdf_with_query'),

    path('task_csv/', InstructorViews.task_csv, name="task_csv"),
    path('task_csv/<str:search_query>/', InstructorViews.task_csv, name='task_csv_with_query'),



    path('check_taskname_exist', InstructorViews.check_taskname_exist, name="check_taskname_exist"),
    path('instructor_lesson_plan', InstructorViews.instructor_lesson_plan, name="instructor_lesson_plan"),
    path('instructor_lesson_plan_save', InstructorViews.instructor_lesson_plan_save,
         name="instructor_lesson_plan_save"),

    path('manage_instructor_lesson_plan', InstructorViews.manage_instructor_lesson_plan,
         name="manage_instructor_lesson_plan"),
    path('manage_instructor_lesson_plan/export_all/', InstructorViews.manage_instructor_lesson_plan,
         {'export_all': True}, name='export_all_lessons'),
    path('edit_instructor_lesson_plan/<str:lp_id>', InstructorViews.edit_instructor_lesson_plan,
         name="edit_instructor_lesson_plan"),
    path('edit_instructor_lesson_plan_save', InstructorViews.edit_instructor_lesson_plan_save,
         name="edit_instructor_lesson_plan_save"),
    path('lesson_pdf/', InstructorViews.lesson_pdf, name='lesson_pdf'),
    path('lesson_pdf/<str:search_query>/', InstructorViews.lesson_pdf, name='lesson_pdf_with_query'),

    path('lesson_csv/', InstructorViews.lesson_csv, name="lesson_csv"),
    path('lesson_csv/<str:search_query>/', InstructorViews.lesson_csv, name='lesson_csv_with_query'),

    path('instructor_add_result', InstructorViews.instructor_add_result,
         name="instructor_add_result"),
    path('instructor_save_result', InstructorViews.instructor_save_result,
         name="instructor_save_result"),
    path('get_students', InstructorViews.get_students, name="get_students"),
    path('staff_fcmtoken_save', InstructorViews.staff_fcmtoken_save, name="staff_fcmtoken_save"),

    path('fetch_notificationsSF/', InstructorViews.fetch_notificationsSF, name='fetch_notificationsSF'),
    path('mark_notification_as_readSF', InstructorViews.mark_notification_as_readSF,
         name="mark_notification_as_readSF"),


    # Examiner URL Path
    path('examiner_home', ExaminerViews.examiner_home, name="examiner_home"),
    path('examiner_profile', ExaminerViews.examiner_profile, name="examiner_profile"),
    path('examiner_profile_save', ExaminerViews.examiner_profile_save, name="examiner_profile_save"),
    path('get_batches_ex/', ExaminerViews.get_batches_ex, name='get_batches_ex'),
    path('get_subjects_ex/', ExaminerViews.get_subjects_ex, name='get_subjects_ex'),
    path('examiner_take_attendance', ExaminerViews.examiner_take_attendance,
         name="examiner_take_attendance"),

    path('examiner_view_attendance', ExaminerViews.examiner_view_attendance,
         name="examiner_view_attendance"),
    path('examiner_view_attendance/export_all/', ExaminerViews.examiner_view_attendance, {'export_all': True},
         name='export_all_exam'),
    path('exam_pdf/', ExaminerViews.exam_pdf, name='exam_pdf'),
    path('exam_pdf/<str:search_query>/', ExaminerViews.exam_pdf, name='exam_pdf_with_query'),
    path('exam_csv/', ExaminerViews.exam_csv, name='exam_csv'),

    path('get_subjects/', ExaminerViews.get_subjects, name='get_subjects'),

    path('generate_daily_exam_report', ExaminerViews.generate_daily_exam_report,
         name="generate_daily_exam_report"),
    path('exam_other_attendance_report', ExaminerViews.exam_other_attendance_report,
         name="exam_other_attendance_report"),

    # Principal URL Path
    path('principal_home', PrincipalViews.principal_home, name="principal_home"),
    path('staff_leave_view', PrincipalViews.staff_leave_view, name="staff_leave_view"),
    path('staff_disapprove_leave/<str:lrs_id>', PrincipalViews.staff_disapprove_leave, name="staff_disapprove_leave"),
    path('staff_approve_leave/<str:lrs_id>', PrincipalViews.staff_approve_leave, name="staff_approve_leave"),

    # P URL Path
    path('p_home', PViews.p_home, name="p_home"),
    path('student_view_attendance', PViews.student_view_attendance, name="student_view_attendance"),
    path('staff_apply_leave', PViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_approve/<str:lrs_id>', PViews.staff_approve, name="staff_approve"),
    path('staff_disapprove/<str:lrs_id>', PViews.staff_disapprove,
         name="staff_disapprove"),

    path('principal_profile', PViews.principal_profile, name="principal_profile"),
    path('principal_profile_save', PViews.principal_profile_save, name="principal_profile_save"),

    # Student URL Path
    path('student_home', StudentViews.student_home, name="student_home"),

    path('student_apply_leave', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', StudentViews.student_apply_leave_save,
         name="student_apply_leave_save"),
    path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save', StudentViews.student_feedback_save, name="student_feedback_save"),

    path('st_view_attendance', StudentViews.st_view_attendance, name="st_view_attendance"),

    path('st_at_pdf/', StudentViews.st_at_pdf, name='st_at_pdf'),
    path('st_at_pdf/<str:search_query>/', StudentViews.st_at_pdf, name='st_at_pdf_with_query'),

    path('st_at_csv/', StudentViews.st_at_csv, name="st_at_csv"),
    path('st_at_csv/<str:search_query>/', StudentViews.st_at_csv, name='st_at_csv_with_query'),

    path('student_profile', StudentViews.student_profile, name="student_profile"),
    path('student_profile_save', StudentViews.student_profile_save, name="student_profile_save"),
    path('make_payment', StudentViews.make_payment, name="make_payment"),
    path('get_stcourse/', StudentViews.get_stcourse, name='get_stcourse'),
    path('get_stbatch/', StudentViews.get_stbatch, name='get_stbatch'),
    path('student_fcmtoken_save', StudentViews.student_fcmtoken_save, name="student_fcmtoken_save"),

path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),

]  # Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                          document_root=settings.STATIC_ROOT)
