from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from mistech.EmailBackEnd import EmailBackEnd


def showDemoPage(request):
    return render(request, "demo.html")


def showLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, email=request.POST.get("email"),
                                         password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "3":
                return HttpResponseRedirect(reverse("student_home"))
            elif user.user_type == "4":
                return HttpResponseRedirect(reverse("instructor_home"))
            elif user.user_type == "5":
                return HttpResponseRedirect(reverse("examiner_home"))
            elif user.user_type == "6":
                return HttpResponseRedirect(reverse("principal_home"))
            else:
                return HttpResponseRedirect(reverse("staff_home"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email + "usertype :" + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def LogoutUser(request):
    logout(request)
    return redirect('/')


def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/10.10.0/firebase-analytics.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyBpKcLWqfxoNFfEADcXN-dh4bo0Yz--x5Q",' \
         '        authDomain: "mistech-cab4d.firebaseapp.com",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "mistech-cab4d",' \
         '        storageBucket: "mistech-cab4d.appspot.com",' \
         '        messagingSenderId: "464139410488",' \
         '        appId: "1:464139410488:web:8ab152fc488bb85fc49acd",' \
         '        measurementId: "G-6QC5H1EVZF"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")