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
    path('files/', views.file_list, name='files'),
    path('delete-files/', views.delete_files, name='delete_files'),
    path('gemini/', views.gemini_view, name='gemini'),
    path('process-files/', views.process_files, name='process_files'),
    path('gemini/status/', views.gemini_files_status, name='gemini_files_status'),
    path('gemini/download/', views.download_gemini_results, name='download_gemini_results'),
    path('gemini/clear/', views.clear_gemini_results, name='clear_gemini_results'),
]
