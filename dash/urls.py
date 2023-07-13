from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.dashboard_view, name='dashboard'),
    path('login/', views.auth.login_view, name='login'),
    path('logout/', views.auth.logout_view, name='logout'),
    path('action/create_file/', views.index.create_file_view, name='create_file'),
]
