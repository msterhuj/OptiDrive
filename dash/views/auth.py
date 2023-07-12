from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.urls import reverse

from api.models import MoniAgent
from dashboard.models import Page, PageMetricGroup, PageIncident


def login_view(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def dashboard_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    agents = MoniAgent.objects.all()

    return render(request, 'dash.html', {
        "user": request.user,
        "agents": agents
    })


def create_agent_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    agent_name = request.POST.get("agent_name", None)
    if agent_name:
        agent = MoniAgent()
        agent.name = agent_name
        agent.token = "random"
        agent.save()
        return render(request, 'admin/add_agent.html', {
            "create_ok": True,
            "token": agent.token
        })
    else:
        return render(request, 'admin/add_agent.html', {
            "create_ok": False
        })