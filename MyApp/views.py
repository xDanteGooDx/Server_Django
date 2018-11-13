from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
from django.template.context_processors import csrf


def index(request):
    return render(request, "MyApp/start_page.html", {'username': auth.get_user(request).username})


def registration(request):
    return render(request, "MyApp/registration.html")


def auth_login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            args['login_error'] = "Пользователь не найден"
            return render(request, "MyApp/auth.html", args)
    else:
        return render(request, "MyApp/auth.html", args)


def auth_logout(request):
    auth.logout(request)
    return redirect("/")
