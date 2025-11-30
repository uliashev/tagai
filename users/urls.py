from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserLoginView, home, settings_view, upload_files
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('settings/', views.settings_view, name='settings'),
    path('upload/', views.upload_files, name='upload_files'),
    path('files/', views.file_list, name='file_list'),
]
