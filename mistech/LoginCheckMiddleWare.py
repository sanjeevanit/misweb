from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'ALLOWALL'
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        print(modulename)
        user = request.user
        # Exclude password reset URLs from redirection

        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "mistech.AdminViews":
                    pass
                elif modulename == "mistech.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "mistech.StaffViews" or modulename == "django.views.static":
                    pass
                elif modulename == "mistech.views" :
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "4":
                if modulename == "mistech.InstructorViews" or modulename == "django.views.static":
                    pass
                elif modulename == "mistech.views" :
                    pass
                else:
                    return HttpResponseRedirect(reverse("instructor_home"))
            elif user.user_type == "5":
                if modulename == "mistech.ExaminerViews" or modulename == "django.views.static":
                    pass
                elif modulename == "mistech.views" :
                    pass
                else:
                    return HttpResponseRedirect(reverse("examiner_home"))
            elif user.user_type == "6":
                if modulename == "mistech.PViews" or modulename == "django.views.static":
                    pass
                elif modulename == "mistech.views" :
                    pass
                else:
                    return HttpResponseRedirect(reverse("p_home"))
            elif user.user_type == "3":
                if modulename == "mistech.StudentViews" or modulename == "django.views.static":
                    pass
                elif modulename == "mistech.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("doLogin") or modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites" or modulename=="mistech.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))
