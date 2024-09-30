from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class SessionYr(models.Model):
    yr_id = models.AutoField(primary_key=True)
    session_start = models.DateField()
    session_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    object = models.Manager()


class CustomUser(AbstractUser):
    user_ty = ((1, "Admin"), (2, "staff"), (3, "Student"), (4, "Instructor"), (5, "Examiner"), (6, "Principal"))
    user_type = models.CharField(default=1, choices=user_ty, max_length=10)
    profile_img = models.ImageField(upload_to='user_img/', null=True)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Trade(models.Model):
    tr_id = models.AutoField(primary_key=True)
    tr_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Course(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=255, unique=True)
    c_code = models.CharField(max_length=255, unique=True)
    c_type = models.CharField(max_length=10)
    c_duration = models.CharField(max_length=4)
    c_qualification = models.CharField(max_length=5, null=True)
    tr_id = models.ForeignKey(Trade, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Batch(models.Model):
    b_id = models.AutoField(primary_key=True)
    b_code = models.CharField(max_length=50, unique=True)
    sem_no = models.CharField(max_length=1)
    c_id = models.ForeignKey(Course, on_delete=models.CASCADE, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Staff(models.Model):
    sf_id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50, null=True)
    dob = models.DateField(null=False)
    adrz = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=10, null=False)
    nic = models.CharField(max_length=20, null=False)
    sf_idNo = models.CharField(max_length=50, unique=True, null=True)
    nationality = models.CharField(max_length=50, null=True)
    civil_status = models.CharField(max_length=10, null=True)
    mobileNo = models.CharField(max_length=12, null=False)
    resiNo = models.CharField(max_length=11, null=True)
    edu_qualification = models.CharField(max_length=10, null=True)
    prof_qualification = models.CharField(max_length=255, null=True)
    other_qualification = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=20, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()


class Subject(models.Model):
    sub_id = models.AutoField(primary_key=True)
    sub_code = models.CharField(max_length=255, unique=True)
    sub_name = models.CharField(max_length=255, unique=True)
    c_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    sf_id = models.ManyToManyField('Staff')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Module(models.Model):
    mod_id = models.AutoField(primary_key=True)
    mod_code = models.CharField(max_length=255, unique=True)
    mod_name = models.CharField(max_length=255)
    duration_hours = models.PositiveIntegerField()
    academic_weeks = models.PositiveIntegerField()
    c_id = models.ForeignKey(Course, on_delete=models.CASCADE, default=True)
    sub_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Student(models.Model):
    st_id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50, null=True)
    dob = models.DateField(null=False)
    adrz = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=10, null=False)
    nic = models.CharField(max_length=20, unique=True, null=False)
    st_idNo = models.CharField(max_length=100, unique=True, null=True)
    nationality = models.CharField(max_length=50, null=True)
    mobileNo = models.CharField(max_length=12, null=False)
    resiNo = models.CharField(max_length=10, null=True)
    civil_status = models.CharField(max_length=10, null=True)
    edu_qualification = models.CharField(max_length=10, null=True)
    prof_qualification = models.CharField(max_length=10, null=True)
    other_qualification = models.CharField(max_length=255, null=True)
    guardian_name = models.CharField(max_length=100, null=True)
    guardian_contNo = models.CharField(max_length=20, null=True)
    yr_id = models.ForeignKey(SessionYr, on_delete=models.DO_NOTHING)
    b_id = models.ForeignKey(Batch, on_delete=models.DO_NOTHING, default=True)
    tr_id = models.ForeignKey(Trade, on_delete=models.DO_NOTHING, default=True)
    c_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()


class Task(models.Model):
    STATUS_CHOICES = [
        ('complete', 'Completed'),
        ('not_complete', 'Not Completed'),
    ]

    tk_id = models.AutoField(primary_key=True)
    tk_name = models.CharField(max_length=255, unique=True)
    tk_date = models.DateField(null=False)
    tk_wk = models.PositiveIntegerField(default=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_complete')
    sf_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    mod_id = models.ForeignKey(Module, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Lplan(models.Model):
    lp_id = models.AutoField(primary_key=True)
    st_activity = models.CharField(max_length=255)
    methodology = models.CharField(max_length=255)
    media = models.CharField(max_length=255)
    lp_time = models.PositiveIntegerField(default=True)
    tk_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    sf_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Attendance(models.Model):
    at_id = models.AutoField(primary_key=True)
    at_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, null=True)
    st_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    yr_id = models.ForeignKey(SessionYr, on_delete=models.CASCADE)
    b_id = models.ForeignKey(Batch, on_delete=models.DO_NOTHING)
    c_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    sub_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    sf_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceE(models.Model):
    ae_id = models.AutoField(primary_key=True)
    ae_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, null=True)
    ex_name = models.CharField(max_length=200, null=False)
    st_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    yr_id = models.ForeignKey(SessionYr, on_delete=models.CASCADE)
    b_id = models.ForeignKey(Batch, on_delete=models.DO_NOTHING)
    c_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    sub_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    sf_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Payment(models.Model):
    pay_id = models.AutoField(primary_key=True)
    st_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    c_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    b_id = models.ForeignKey(Batch, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportS(models.Model):
    lr_id = models.AutoField(primary_key=True)
    lr_date = models.DateField(null=False)
    lr_msg = models.TextField()
    lr_status = models.IntegerField(default=0)
    st_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportSf(models.Model):
    lrs_id = models.AutoField(primary_key=True)
    lrs_date = models.DateField(null=False)
    lrs_msg = models.TextField()
    lrs_status = models.IntegerField(default=0)
    medical_img = models.ImageField(upload_to='medical_img/', null=True)
    reason_lv = models.TextField(null=True)
    sf_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackS(models.Model):
    fb_id = models.AutoField(primary_key=True)
    fb = models.CharField(max_length=255)
    fb_rpy = models.TextField()
    st_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedbackSf(models.Model):
    fbs_id = models.AutoField(primary_key=True)
    fbs = models.CharField(max_length=255)
    fbs_rpy = models.TextField()
    sf_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    sr_id = models.AutoField(primary_key=True)
    st_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    sub_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    sub_exam_marks = models.FloatField(default=0)
    sub_asgn_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationS(models.Model):
    nfy_id = models.AutoField(primary_key=True)
    notify = models.TextField()
    st_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationSf(models.Model):
    nfysf_id = models.AutoField(primary_key=True)
    notify_sf = models.TextField()
    sf_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)  # Add a field to track whether the notification has been read
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance, dob="2022-01-01")
        if instance.user_type == 3:
            Student.objects.create(admin=instance, dob="2022-01-01", yr_id=SessionYr.object.get(yr_id=1),
                                   c_id=Course.objects.get(c_id=1),
                                   tr_id=Trade.objects.get(tr_id=1))
        if instance.user_type == 4:
            Staff.objects.create(admin=instance, dob="2022-01-01")
        if instance.user_type == 5:
            Staff.objects.create(admin=instance, dob="2022-01-01")
        if instance.user_type == 6:
            Staff.objects.create(admin=instance, dob="2022-01-01")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
    if instance.user_type == 4:
        instance.staff.save()
    if instance.user_type == 5:
        instance.staff.save()
    if instance.user_type == 6:
        instance.staff.save()
