from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def dashboard_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))


    return render(request, 'dash.html', {
        "user": request.user,
    })