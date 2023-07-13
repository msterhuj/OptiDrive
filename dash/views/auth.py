from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.urls import reverse


def login_view(request):
    """
    Login view
    redirect to dashboard if user is authenticated
    manage login form
    """
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    if request.user.is_authenticated:
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'auth/login.html')


def logout_view(request):
    """
    Logout user and redirect to login page
    """
    logout(request)
    return HttpResponseRedirect(reverse('login'))

