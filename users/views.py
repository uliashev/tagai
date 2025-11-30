from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
import os
from .forms import UserLoginForm, SettingsForm

class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

@login_required
def home(request):
    return render(request, 'users/dashboard.html')

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully.')
            return redirect('settings')
    else:
        form = SettingsForm(instance=request.user)
    
    return render(request, 'users/settings.html', {'form': form})

@login_required
@require_POST
def upload_files(request):
    files = request.FILES.getlist('files')
    
    if not files:
        return JsonResponse({'error': 'No files provided'}, status=400)
        
    if len(files) > 20:
        return JsonResponse({'error': 'Maximum 20 files allowed'}, status=400)
        
    upload_dir = settings.TEMP_UPLOAD_DIR
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    for file in files:
        file_path = upload_dir / file.name
        # Handle duplicate filenames if necessary, for now just overwrite or save
        # To be safe, maybe we should append a timestamp or uuid, but the requirement is simple.
        # Let's just save it.
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        saved_files.append(file.name)
        
    return JsonResponse({'message': f'Successfully uploaded {len(saved_files)} files', 'files': saved_files})

@login_required
def file_list(request):
    upload_dir = settings.TEMP_UPLOAD_DIR
    files = []
    if upload_dir.exists():
        files = [f.name for f in upload_dir.iterdir() if f.is_file()]
    
    return render(request, 'users/files.html', {'files': files})
