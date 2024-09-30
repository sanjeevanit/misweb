from datetime import datetime

from django import forms
from django.forms import ChoiceField, formset_factory

from mistech.models import Trade, Course, Subject, SessionYr, Staff, Batch, Module, Task


class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass


class DateInput(forms.DateInput):
    input_type = "date"


class AddTradeForm(forms.Form):
    tr_name = forms.CharField(label="Trade Name", max_length=255,
                              widget=forms.TextInput(attrs={"class": "form-control"}))


class EditTradeForm(forms.Form):
    tr_name = forms.CharField(label="Trade Name", max_length=255,
                              widget=forms.TextInput(attrs={"class": "form-control"}))


class AddStudentForm(forms.Form):
    profile_img = forms.ImageField(label="Profile Image", max_length=50,
                                   widget=forms.FileInput(attrs={"class": "form-control", "id": "fileupload"}))

    first_name = forms.CharField(label="First Name", max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    middle_name = forms.CharField(max_length=50,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="User Name", max_length=100,
                               widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}))
    email = forms.EmailField(label="Email", max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "off"}))
    password = forms.CharField(label="Password", max_length=100,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    dob = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))

    gender_choice = (("M", "Male"), ("F", "Female"))
    gender = forms.ChoiceField(choices=gender_choice,
                               widget=forms.Select(attrs={"class": "form-control select2 select2-danger"}))

    adrz = forms.CharField(label="Course Code", max_length=255,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    nic = forms.CharField(label="Course Code", max_length=20,
                          widget=forms.TextInput(attrs={"class": "form-control"}))
    st_idNo = forms.CharField(label="Course Code", max_length=100,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    nationality = forms.CharField(label="Course Code", max_length=50,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    status_choice = (("M", "Married"), ("UM", "Unmarried"))
    civil_status = forms.ChoiceField(choices=status_choice,
                                     widget=forms.Select(attrs={"class": "form-control select2 select2-danger"}))

    mobileNo = forms.CharField(label="Course Code", max_length=10,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    resiNo = forms.CharField(label="Course Code", max_length=10,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    edu_choice = (("OL", "O/L"), ("AL", "A/L"))
    edu_qualification = forms.ChoiceField(choices=edu_choice, widget=forms.Select(
        attrs={"class": "select2  form-control", "multiple": "multiple"}))

    prof_choice = (("NVQ1", "NVQ 01"), ("NVQ2", "NVQ 02"), ("NVQ3", "NVQ 03"), ("NVQ4", "NVQ 04"), ("NVQ5", "NVQ 05"),
                   ("NVQ6", "NVQ 06"), ("Certi", "Certificate"), ("Dip", "Diploma"))
    prof_qualification = forms.ChoiceField(choices=prof_choice, widget=forms.Select(
        attrs={"class": "select2 form-control", "multiple": "multiple"}))

    other_qualification = forms.CharField(label="Other Qualification", max_length=255,
                                          widget=forms.TextInput(attrs={"class": "form-control"}))
    guardian_name = forms.CharField(label="Guardian Name", max_length=50,
                                    widget=forms.TextInput(attrs={"class": "form-control"}))
    guardian_contNo = forms.CharField(label="Guardian Contact No", max_length=20,
                                      widget=forms.TextInput(attrs={"class": "form-control"}))
    session_list = []
    try:
        sessions = SessionYr.object.all()

        for ses in sessions:
            a_ses = (ses.yr_id, str(ses.session_start) + "   To  " + str(ses.session_end))
            session_list.append(a_ses)
    except:
        session_list = []
    yr_id = forms.ChoiceField(label="Session Year", choices=session_list,
                              widget=forms.Select(attrs={"class": "select2 form-control"}))

    bt_list = []
    try:
        batch = Batch.objects.all()
        for batch in batch:
            bt = (batch.b_id, batch.b_code)
            bt_list.append(bt)
    except:
        bt_list = []
    batch = forms.ChoiceField(label="Batch Code", choices=bt_list,
                              widget=forms.Select(attrs={"class": "select2 form-control"}))

    tr_list = []
    try:
        trades = Trade.objects.all()
        for trade in trades:
            td = (trade.tr_id, trade.tr_name)
            tr_list.append(td)
    except:
        tr_list = []
    trade = forms.ChoiceField(label="Trade Name", choices=tr_list,
                              widget=forms.Select(attrs={"class": "select2 form-control"}))
    coz_list = []
    try:
        course = Course.objects.all()
        for course in course:
            coz = (course.c_id, course.c_name)
            coz_list.append(coz)
    except:
        coz_list = []
    course = forms.ChoiceField(label="Course Name", choices=coz_list,
                               widget=forms.Select(attrs={"class": "select2 form-control"}))


class EditStudentForm(forms.Form):
    profile_img = forms.ImageField(label="Profile Image", max_length=50,
                                   widget=forms.FileInput(attrs={"class": "form-control"}), required=False)

    first_name = forms.CharField(label="First Name", max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    middle_name = forms.CharField(max_length=50,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="User Name", max_length=100,
                               widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}))
    email = forms.EmailField(label="Email", max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "off"}))
    dob = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))

    gender_choice = (("M", "Male"), ("F", "Female"))
    gender = forms.ChoiceField(choices=gender_choice,
                               widget=forms.Select(attrs={"class": "form-control select2 select2-danger"}))

    adrz = forms.CharField(label="Course Code", max_length=255,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    nic = forms.CharField(label="Course Code", max_length=20,
                          widget=forms.TextInput(attrs={"class": "form-control"}))
    st_idNo = forms.CharField(label="Course Code", max_length=100,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    nationality = forms.CharField(label="Course Code", max_length=50,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    status_choice = (("M", "Married"), ("UM", "Unmarried"))
    civil_status = forms.ChoiceField(choices=status_choice,
                                     widget=forms.Select(attrs={"class": "form-control select2 select2-danger"}))

    mobileNo = forms.CharField(label="Course Code", max_length=10,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    resiNo = forms.CharField(label="Course Code", max_length=10,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    edu_choice = (("OL", "O/L"), ("AL", "A/L"))
    edu_qualification = forms.ChoiceField(choices=edu_choice, widget=forms.Select(
        attrs={"class": "select2  form-control", "multiple": "multiple"}))

    prof_choice = (("NVQ1", "NVQ 01"), ("NVQ2", "NVQ 02"), ("NVQ3", "NVQ 03"), ("NVQ4", "NVQ 04"), ("NVQ5", "NVQ 05"),
                   ("NVQ6", "NVQ 06"), ("Certi", "Certificate"), ("Dip", "Diploma"))
    prof_qualification = forms.ChoiceField(choices=prof_choice, widget=forms.Select(
        attrs={"class": "select2 form-control", "multiple": "multiple"}))

    other_qualification = forms.CharField(label="Other Qualification", max_length=255,
                                          widget=forms.TextInput(attrs={"class": "form-control"}))
    guardian_name = forms.CharField(label="Guardian Name", max_length=50,
                                    widget=forms.TextInput(attrs={"class": "form-control"}))
    guardian_contNo = forms.CharField(label="Guardian Contact No", max_length=20,
                                      widget=forms.TextInput(attrs={"class": "form-control"}))
    session_list = []
    try:
        sessions = SessionYr.object.all()

        for ses in sessions:
            a_ses = (ses.yr_id, str(ses.session_start) + "   To  " + str(ses.session_end))
            session_list.append(a_ses)
    except:
        session_list = []
    yr_id = forms.ChoiceField(label="Session Year", choices=session_list,
                              widget=forms.Select(attrs={"class": "select2 form-control"}))

    bt_list = []
    try:
        batch = Batch.objects.all()
        for batch in batch:
            bt = (batch.b_id, batch.b_code)
            bt_list.append(bt)
    except:
        bt_list = []
    batch = forms.ChoiceField(label="Batch Code", choices=bt_list,
                              widget=forms.Select(attrs={"class": "select2 form-control"}))

    tr_list = []
    try:
        trades = Trade.objects.all()
        for trade in trades:
            td = (trade.tr_id, trade.tr_name)
            tr_list.append(td)
    except:
        tr_list = []
    trade = forms.ChoiceField(label="Trade Name", choices=tr_list,
                              widget=forms.Select(attrs={"class": "select2 form-control"}))
    coz_list = []
    try:
        course = Course.objects.all()
        for course in course:
            coz = (course.c_id, course.c_name)
            coz_list.append(coz)
    except:
        coz_list = []
    course = forms.ChoiceField(label="Course Name", choices=coz_list,
                               widget=forms.Select(attrs={"class": "select2 form-control"}))


class AddStaffForm(forms.Form):
    profile_img = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control", "id": "fileupload"}))

    first_name = forms.CharField(label="First Name", max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    middle_name = forms.CharField(max_length=50,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="User Name", max_length=100,
                               widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}))
    email = forms.EmailField(label="Email", max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "off"}))
    password = forms.CharField(label="Password", max_length=100,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    dob = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))

    gender_choice = (("M", "Male"), ("F", "Female"))
    gender = forms.ChoiceField(choices=gender_choice,
                               widget=forms.Select(attrs={"class": "form-control select2 select2-danger"}))

    adrz = forms.CharField(label="Course Code", max_length=255,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    nic = forms.CharField(label="Course Code", max_length=20,
                          widget=forms.TextInput(attrs={"class": "form-control"}))
    sf_idNo = forms.CharField(label="Course Code", max_length=100,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    nationality = forms.CharField(label="Course Code", max_length=50,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    status_choice = (("M", "Married"), ("UM", "Unmarried"))
    civil_status = forms.ChoiceField(choices=status_choice,
                                     widget=forms.Select(attrs={"class": "form-control select2 select2-purple"}))
    mobileNo = forms.CharField(label="Course Code", max_length=10,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    resiNo = forms.CharField(label="Course Code", max_length=10,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    edu_choice = (("OL", "O/L"), ("AL", "A/L"))
    edu_qualification = forms.ChoiceField(choices=edu_choice, widget=forms.Select(
        attrs={"class": "select2  form-control"}))

    prof_choice = (
        ("Diploma", "Diploma"), ("Degree", "Degree"), ("Hons", "Special Degree"),
        ("PostGraduate", "Post Graduate Diploma"),
        ("Masters", "Masters Degree"), ("Mphil", "Mphil"), ("PhD", "PhD"))
    prof_qualification = forms.ChoiceField(choices=prof_choice, widget=forms.Select(
        attrs={"class": "select2 form-control"}))

    other_qualification = forms.CharField(label="Other Qualification", max_length=255,
                                          widget=forms.TextInput(attrs={"class": "form-control"}))
    position_choice = (
        ("Instructor", "Instructor"), ("Examiner", "Examiner"), ("Lecturer", "Lecturer"), ("Principal", "Principal"),
        ("OtherStaff", "Other Staff")
    )
    position = forms.ChoiceField(choices=position_choice,
                                 widget=forms.Select(attrs={"class": "select2 form-control"}))


class EditStaffForm(forms.Form):
    profile_img = forms.ImageField(label="Profile Image", max_length=50,
                                   widget=forms.FileInput(attrs={"class": "form-control", "id": "fileupload"}),
                                   required=False)

    first_name = forms.CharField(label="First Name", max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    middle_name = forms.CharField(max_length=50,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="User Name", max_length=100,
                               widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}))
    email = forms.EmailField(label="Email", max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "off"}))

    dob = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))

    gender_choice = (("M", "Male"), ("F", "Female"))
    gender = forms.ChoiceField(choices=gender_choice,
                               widget=forms.Select(attrs={"class": "form-control select2 select2-danger"}))

    adrz = forms.CharField(label="Course Code", max_length=255,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    nic = forms.CharField(label="Course Code", max_length=20,
                          widget=forms.TextInput(attrs={"class": "form-control"}))
    sf_idNo = forms.CharField(label="Course Code", max_length=100,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    nationality = forms.CharField(label="Course Code", max_length=50,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    status_choice = (("M", "Married"), ("UM", "Unmarried"))
    civil_status = forms.ChoiceField(choices=status_choice,
                                     widget=forms.Select(attrs={"class": "form-control select2 select2-purple"}))
    mobileNo = forms.CharField(label="Course Code", max_length=10,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    resiNo = forms.CharField(label="Course Code", max_length=10,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    edu_choice = (("OL", "O/L"), ("AL", "A/L"))
    edu_qualification = forms.ChoiceField(choices=edu_choice, widget=forms.Select(
        attrs={"class": "select2  form-control"}))

    prof_choice = (
        ("Diploma", "Diploma"), ("Degree", "Degree"), ("Hons", "Special Degree"),
        ("PostGraduate", "Post Graduate Diploma"),
        ("Masters", "Masters Degree"), ("Mphil", "Mphil"), ("PhD", "PhD"))
    prof_qualification = forms.ChoiceField(choices=prof_choice, widget=forms.Select(
        attrs={"class": "select2 form-control"}))

    other_qualification = forms.CharField(label="Other Qualification", max_length=255,
                                          widget=forms.TextInput(attrs={"class": "form-control"}))
    position_choice = (
        ("Instructor", "Instructor"), ("Examiner", "Examiner"), ("Lecturer", "Lecturer"), ("Principal", "Principal"),
        ("OtherStaff", "Other Staff")
    )
    position = forms.ChoiceField(choices=position_choice,
                                 widget=forms.Select(attrs={"class": "select2 form-control"}))


class AddCourseForm(forms.Form):
    c_name = forms.CharField(label="Course Name", max_length=255,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    c_code = forms.CharField(label="Course Code", max_length=255,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    type_choice = (("FT", "Full Time"), ("PT", "Part Time"))
    c_type = forms.ChoiceField(label="Type", choices=type_choice,
                               widget=forms.Select(attrs={"class": "select2 form-control"}))

    duration_choice = (
        ("3M", "3 Months"), ("6M", "6 Months"), ("12M", "1 Year"), ("18M", "1 Year 6 Months"), ("24M", "2 Year"),
        ("30M", "2 Year 6 Months"),
        ("36M", "3 Year"), ("42M", "3 Year 6Months"), ("48M", "4 Year"))
    c_duration = forms.ChoiceField(label="Duration", choices=duration_choice,
                                   widget=forms.Select(attrs={"class": "select2 form-control"}))

    qul_choice = (("NVQ1", "NVQ 01"), ("NVQ2", "NVQ 02"), ("NVQ3", "NVQ 03"), ("NVQ4", "NVQ 04"), ("NVQ5", "NVQ 05"),
                  ("NVQ6", "NVQ 06"), ("Certi", "Certificate"), ("Dip", "Diploma"))
    c_qualification = forms.ChoiceField(label="Qualification", choices=qul_choice,
                                        widget=forms.Select(attrs={"class": "select2 form-control"}))
    tr_list = []
    try:
        trades = Trade.objects.all()
        for trade in trades:
            td = (trade.tr_id, trade.tr_name)
            tr_list.append(td)
    except:
        tr_list = []
    trade = forms.ChoiceField(label="Trade Name", choices=tr_list,
                              widget=forms.Select(attrs={"class": "select2 form-control"}))


class EditCourseForm(forms.Form):
    c_name = forms.CharField(label="Course Name", max_length=255,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    c_code = forms.CharField(label="Course Code", max_length=255,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    type_choice = (("FT", "Full Time"), ("PT", "Part Time"))
    c_type = forms.ChoiceField(label="Type", choices=type_choice,
                               widget=forms.Select(attrs={"class": "select2 form-control"}))

    duration_choice = (
        ("3M", "3 Months"), ("6M", "6 Months"), ("12M", "1 Year"), ("18M", "1 Year 6 Months"), ("24M", "2 Year"),
        ("30M", "2 Year 6 Months"),
        ("36M", "3 Year"), ("42M", "3 Year 6Months"), ("48M", "4 Year"))
    c_duration = forms.ChoiceField(label="Duration", choices=duration_choice,
                                   widget=forms.Select(attrs={"class": "select2 form-control"}))

    qul_choice = (("NVQ1", "NVQ 01"), ("NVQ2", "NVQ 02"), ("NVQ3", "NVQ 03"), ("NVQ4", "NVQ 04"), ("NVQ5", "NVQ 05"),
                  ("NVQ6", "NVQ 06"), ("Certi", "Certificate"), ("Dip", "Diploma"))
    c_qualification = forms.ChoiceField(label="Qualification", choices=qul_choice,
                                        widget=forms.Select(attrs={"class": "select2 form-control"}))

    tr_list = []
    try:
        trades = Trade.objects.all()
        for trade in trades:
            td = (trade.tr_id, trade.tr_name)
            tr_list.append(td)
    except:
        tr_list = []
    trade = forms.ChoiceField(label="Trade Name", choices=tr_list,
                              widget=forms.Select(attrs={"class": "select2 form-control"}))


class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['sub_name', 'sub_code', 'c_id', 'sf_id']
        labels = {
            'sub_name': 'Subject Name',
            'sub_code': 'Subject Code',
            'c_id': 'Course Name',
            'sf_id': 'Staff ID No',
        }
        widgets = {
            'sub_name': forms.TextInput(attrs={"class": "form-control"}),
            'sub_code': forms.TextInput(attrs={"class": "form-control"}),
            'c_id': forms.Select(attrs={"class": "select2 form-control"}),
            'sf_id': forms.SelectMultiple(attrs={"class": "select2 form-control"}),
        }


class EditSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['sub_name', 'sub_code', 'c_id', 'sf_id']
        labels = {
            'sub_name': 'Subject Name',
            'sub_code': 'Subject Code',
            'c_id': 'Course Name',
            'sf_id': 'Staff ID No',
        }
        widgets = {
            'sub_name': forms.TextInput(attrs={"class": "form-control"}),
            'sub_code': forms.TextInput(attrs={"class": "form-control"}),
            'c_id': forms.Select(attrs={"class": "select2 form-control", "c_id": "id_course"}),
            'sf_id': forms.SelectMultiple(attrs={"class": "select2 form-control", "sf_id": "id_sf_id"}),
        }


class AddBatchForm(forms.Form):
    b_year = forms.IntegerField(
        label="Batch Year",
        widget=forms.Select(
            choices=[(year, year) for year in range(datetime.now().year, datetime.now().year - 30, -1)],
            attrs={"class": "select2 form-control"}
        )
    )
    cos_list = []
    try:
        course_n = Course.objects.all()
        for course_n in course_n:
            cos = (course_n.c_id, course_n.c_code)
            cos_list.append(cos)
    except:
        cos_list = []
    course_n = forms.ChoiceField(label="Course Name", choices=cos_list,
                                 widget=forms.Select(attrs={"class": "select2 form-control"}))
    batch = (("B1", "B1"), ("B2", "B2"), ("B3", "B3"), ("B4", "B4"), ("B5", "B5"),
             ("B6", "B6"))
    b_no = forms.ChoiceField(label="Batch No", choices=batch,
                             widget=forms.Select(attrs={"class": "select2 form-control"}))
    sem_choice = (
        ("1", "Semester 01"), ("2", "Semester 02"), ("3", "Semester 03"), ("4", "Semester 04"), ("5", "Semester 05"),
        ("6", "Semester 06"), ("7", "Semester 07"), ("8", "Semester 08"), ("9", "Semester 09"))
    sem_no = forms.ChoiceField(label="Semester", choices=sem_choice,
                               widget=forms.Select(attrs={"class": "select2 form-control"}))

    coz_list = []
    try:
        course = Course.objects.all()
        for course in course:
            coz = (course.c_id, course.c_name)
            coz_list.append(coz)
    except:
        coz_list = []
    course = forms.ChoiceField(label="Course Code", choices=coz_list,
                               widget=forms.Select(attrs={"class": "select2 form-control"}))







class EditBatchForm(forms.Form):
    bh_list = []
    try:
        batch = Batch.objects.all()
        for batch in batch:
            bh = (batch.b_id, batch.b_code)
            bh_list.append(bh)
    except:
        bh_list = []
    bath = forms.ChoiceField(label="Batch Code", choices=bh_list,
                             widget=forms.Select(attrs={"class": "select2 form-control"}))

    sem_choice = (
        ("1", "Semester 01"), ("2", "Semester 02"), ("3", "Semester 03"), ("4", "Semester 04"), ("5", "Semester 05"),
        ("6", "Semester 06"), ("7", "Semester 07"), ("8", "Semester 08"), ("9", "Semester 09"))
    sem_no = forms.ChoiceField(label="Semester", choices=sem_choice,
                               widget=forms.Select(attrs={"class": "select2 form-control"}))
    cos_list = []
    try:
        course_n = Course.objects.all()
        for course_n in course_n:
            cos = (course_n.c_id, course_n.c_name)
            cos_list.append(cos)
    except:
        cos_list = []
    course_n = forms.ChoiceField(label="Course Name", choices=cos_list,
                                 widget=forms.Select(attrs={"class": "select2 form-control"}))


class AddModuleForm(forms.Form):
    mod_name = forms.CharField(label="Module Name", max_length=255,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    mod_code = forms.CharField(label="Module Code", max_length=255,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    duration_hours = forms.IntegerField(label="Duration Hours",
                                        widget=forms.TextInput(attrs={"class": "form-control", "id": "duration_hours"}))
    academic_weeks = forms.IntegerField(label="Academic Weeks",
                                        widget=forms.TextInput(attrs={"class": "form-control", "id": "academic_weeks"}))

    coz_list = []
    try:
        course = Course.objects.all()
        for course in course:
            coz = (course.c_id, course.c_name)
            coz_list.append(coz)
    except:
        coz_list = []
    course = forms.ChoiceField(label="Course Name", choices=coz_list,
                               widget=forms.Select(
                                   attrs={"class": "select2 form-control", "onchange": "fetchSubjects(this.value)"}))

    sub_list = []
    try:
        subjects = Subject.objects.all()
        for subject in subjects:
            td = (subject.sub_id, subject.sub_name)
            sub_list.append(td)
    except:
        sub_list = []
    subject = forms.ChoiceField(label="Subject Name", choices=sub_list,
                                widget=forms.Select(attrs={"class": "select2 form-control", "id": "id_subject"}))


class EditModuleForm(forms.Form):
    mod_name = forms.CharField(label="Module Name", max_length=255,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    mod_code = forms.CharField(label="Module Code", max_length=255,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    duration_hours = forms.IntegerField(label="Duration Hours",
                                        widget=forms.TextInput(attrs={"class": "form-control", "id": "duration_hours"}))
    academic_weeks = forms.IntegerField(label="Academic Weeks",
                                        widget=forms.TextInput(attrs={"class": "form-control", "id": "academic_weeks"}))

    coz_list = []
    try:
        course = Course.objects.all()
        for course in course:
            coz = (course.c_id, course.c_name)
            coz_list.append(coz)
    except:
        coz_list = []
    course = forms.ChoiceField(label="Course Name", choices=coz_list,
                               widget=forms.Select(
                                   attrs={"class": "select2 form-control", "onchange": "fetchSubjects(this.value)"}))

    sub_list = []
    try:
        subjects = Subject.objects.all()
        for subject in subjects:
            td = (subject.sub_id, subject.sub_name)
            sub_list.append(td)
    except:
        sub_list = []
    subject = forms.ChoiceField(label="Subject Name", choices=sub_list,
                                widget=forms.Select(attrs={"class": "select2 form-control", "id": "id_subject"}))


class AddLessonForm(forms.Form):
    tk_list = []
    try:
        task = Task.objects.all()
        for task in task:
            tk = (task.tk_id, task.tk_name)
            tk_list.append(tk)
    except:
        coz_list = []
    task = forms.ChoiceField(label="Instructor Activity", choices=tk_list,
                             widget=forms.Select(attrs={"class": "select2 form-control"}))
    st_activity = forms.CharField(label="Student Activity", max_length=255,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    methodology = forms.CharField(label="Methodology", max_length=255,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    media = forms.CharField(label="Required Media", max_length=255,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    lp_time = forms.IntegerField(label="Time",
                                 widget=forms.TextInput(attrs={"class": "form-control", "id": "lp_time"}))


class EditLessonForm(forms.Form):
    tk_list = []
    try:
        task = Task.objects.all()
        for task in task:
            tk = (task.tk_id, task.tk_name)
            tk_list.append(tk)
    except:
        coz_list = []
    task = forms.ChoiceField(label="Instructor Activity", choices=tk_list,
                             widget=forms.Select(attrs={"class": "select2 form-control"}))
    st_activity = forms.CharField(label="Student Activity", max_length=255,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    methodology = forms.CharField(label="Methodology", max_length=255,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    media = forms.CharField(label="Required Media", max_length=255,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    lp_time = forms.IntegerField(label="Time",
                                 widget=forms.TextInput(attrs={"class": "form-control", "id": "lp_time"}))


class PaymentForm(forms.Form):
    coz_list = []
    try:
        course = Course.objects.all()
        for course in course:
            coz = (course.c_id, course.c_name)
            coz_list.append(coz)
    except:
        coz_list = []
    course = forms.ChoiceField(label="Course Name", choices=coz_list,
                               widget=forms.Select(attrs={"class": "select2 form-control"}))

    bt_list = []
    try:
        batch = Batch.objects.all()
        for batch in batch:
            bt = (batch.b_id, batch.b_code)
            bt_list.append(bt)
    except:
        bt_list = []
    batch = forms.ChoiceField(label="Batch Code", choices=bt_list,
                              widget=forms.Select(attrs={"class": "select2 form-control"}))

    amount = forms.DecimalField(max_digits=10, decimal_places=2,
                                widget=forms.NumberInput(attrs={"class": "form-control"}))

    card_number = forms.CharField(label='Card Number', required=True,
                                  widget=forms.TextInput(attrs={"class": "form-control"}), )
    exp_month = forms.IntegerField(label='Expiry Month', required=True,
                                   widget=forms.NumberInput(attrs={"class": "form-control"}))
    exp_year = forms.IntegerField(label='Expiry Year', required=True,
                                  widget=forms.NumberInput(attrs={"class": "form-control"}))
    cvc = forms.CharField(label='CVC', required=True, widget=forms.TextInput(attrs={"class": "form-control"}))


class AddTermForm(forms.Form):
    tk_wk = forms.IntegerField(label="Week No",
                               widget=forms.TextInput(attrs={"class": "form-control", "id": "academic_weeks"}))
    mod_list = [(module.mod_id, module.mod_name) for module in Module.objects.all()]
    module = forms.ChoiceField(label="Module Name", choices=mod_list,
                               widget=forms.Select(attrs={"class": "select2 form-control"}))
    tk_name = forms.CharField(label="Task Name", max_length=255,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    tk_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    status = forms.ChoiceField(label="Status", choices=[('complete', 'Complete'), ('not_complete', 'Not Complete')],
                               widget=forms.Select(attrs={"class": "form-control"}))

class EditTermForm(forms.Form):
    tk_wk = forms.IntegerField(label="Week No",
                               widget=forms.TextInput(attrs={"class": "form-control", "id": "academic_weeks"}))
    mod_list = [(module.mod_id, module.mod_name) for module in Module.objects.all()]
    module = forms.ChoiceField(label="Module Name", choices=mod_list,
                               widget=forms.Select(attrs={"class": "select2 form-control"}))
    tk_name = forms.CharField(label="Task Name", max_length=255,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    tk_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    status = forms.ChoiceField(label="Status", choices=[('complete', 'Complete'), ('not_complete', 'Not Complete')],
                               widget=forms.Select(attrs={"class": "form-control"}))




