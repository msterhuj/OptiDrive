from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from files.models import Items


def dashboard_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    items = Items.objects.filter(owner=request.user, is_deleted=False)

    return render(request, 'dash.html', {
        "user": request.user,
        "items": items,
    })


def create_file_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        item = Items()
        item.name = request.POST.get('name')
        item.content = request.POST.get('content')
        item.is_file = True
        if request.POST.get('parent'):
            item.parent = Items.objects.get(pk=request.POST.get('parent'))
        item.owner = request.user
        item.save()
        return HttpResponseRedirect(reverse('dashboard'))

    return render(request, 'file_new.html', {
        "user": request.user,
    })


def create_folder_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        item = Items()
        item.name = request.POST.get('name')
        item.content = request.POST.get('content')
        item.is_file = False
        if request.POST.get('parent'):
            item.parent = Items.objects.get(pk=request.POST.get('parent'))
        item.owner = request.user
        item.save()
        return HttpResponseRedirect(reverse('dashboard'))

    return render(request, 'file_new.html', {
        "user": request.user,
    })