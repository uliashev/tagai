import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
import os
import shutil
from .forms import UserLoginForm, GeminiSettingsForm, OpenAISettingsForm


logger = logging.getLogger(__name__)
class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

@login_required
def home(request):
    return render(request, 'users/dashboard.html', {'max_upload_files': settings.MAX_UPLOAD_FILES})

@login_required
def settings_view(request):
    gemini_form = GeminiSettingsForm(instance=request.user)
    openai_form = OpenAISettingsForm(instance=request.user)

    if request.method == 'POST':
        if 'submit_gemini' in request.POST:
            gemini_form = GeminiSettingsForm(request.POST, instance=request.user)
            if gemini_form.is_valid():
                gemini_form.save()
                messages.success(request, 'Gemini settings updated successfully.')
                return redirect('settings')
        elif 'submit_openai' in request.POST:
            openai_form = OpenAISettingsForm(request.POST, instance=request.user)
            if openai_form.is_valid():
                openai_form.save()
                messages.success(request, 'OpenAI settings updated successfully.')
                return redirect('settings')
    
    return render(request, 'users/settings.html', {
        'gemini_form': gemini_form,
        'openai_form': openai_form
    })

@login_required
@require_POST
def upload_files(request):
    files = request.FILES.getlist('files')
    
    if not files:
        return JsonResponse({'error': 'No files provided'}, status=400)
        
    upload_dir = settings.TEMP_UPLOAD_DIR / str(request.user.id)
    
    current_file_count = 0
    if upload_dir.exists():
        current_file_count = len([f for f in upload_dir.iterdir() if f.is_file()])

    if current_file_count + len(files) > settings.MAX_UPLOAD_FILES:
        return JsonResponse({
            'error': f'Upload limit exceeded. You have {current_file_count} files and can upload {settings.MAX_UPLOAD_FILES - current_file_count} more.'
        }, status=400)

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
    upload_dir = settings.TEMP_UPLOAD_DIR / str(request.user.id)
    files = []
    if upload_dir.exists():
        files = [f.name for f in upload_dir.iterdir() if f.is_file()]
    
    return render(request, 'users/files.html', {'files': files})

@login_required
@require_POST
def delete_files(request):
    upload_dir = settings.TEMP_UPLOAD_DIR / str(request.user.id)
    if upload_dir.exists():
        # Remove all files in the directory
        for file in upload_dir.iterdir():
            if file.is_file():
                file.unlink()
        messages.success(request, 'All files deleted successfully.')
    else:
        messages.info(request, 'No files to delete.')
        
    return redirect('files')

@login_required
def gemini_view(request):
    upload_dir = settings.TEMP_UPLOAD_DIR / str(request.user.id)
    files = []
    processed_files = []
    failed_files = []
    
    if upload_dir.exists():
        # Files that are NOT failed and NOT directories
        files = [f.name for f in upload_dir.iterdir() if f.is_file() and not f.name.endswith('.failed')]
        
        # Processed files
        processed_dir = upload_dir / 'discribed_gemini'
        if processed_dir.exists():
            processed_files = [f.name for f in processed_dir.iterdir() if f.is_file()]
            
        # Failed files (in the same dir, ending with .failed)
        failed_files = [f.name.replace('.failed', '') for f in upload_dir.iterdir() if f.is_file() and f.name.endswith('.failed')]
    
    return render(request, 'users/gemini.html', {
        'files': files,
        'processed_files': processed_files,
        'failed_files': failed_files
    })

@login_required
def gemini_files_status(request):
    upload_dir = settings.TEMP_UPLOAD_DIR / str(request.user.id)
    files = []
    processed_files = []
    failed_files = []
    
    if upload_dir.exists():
        files = [f.name for f in upload_dir.iterdir() if f.is_file() and not f.name.endswith('.failed')]
        
        processed_dir = upload_dir / 'discribed_gemini'
        if processed_dir.exists():
            processed_files = [f.name for f in processed_dir.iterdir() if f.is_file()]
            
        failed_files = [f.name.replace('.failed', '') for f in upload_dir.iterdir() if f.is_file() and f.name.endswith('.failed')]
            
    return JsonResponse({
        'processing': files,
        'processed': processed_files,
        'failed': failed_files
    })

@login_required
@require_POST
def process_files(request):
    logger.info('Processing files')
    upload_dir = settings.TEMP_UPLOAD_DIR / str(request.user.id)
    if not upload_dir.exists():
        return JsonResponse({'error': 'No files to process'}, status=400)
    
    # Get normal files
    files = [f for f in upload_dir.iterdir() if f.is_file() and not f.name.endswith('.failed')]
    
    # Also check for failed files to retry
    failed_files_paths = [f for f in upload_dir.iterdir() if f.is_file() and f.name.endswith('.failed')]
    
    # Rename failed files back to normal to retry them
    for f in failed_files_paths:
        original_name = f.name.replace('.failed', '')
        original_path = upload_dir / original_name
        f.rename(original_path)
        files.append(original_path)
    
    if not files:
        return JsonResponse({'error': 'No files to process'}, status=400)
        
    # Import here to avoid circular imports if any, though unlikely given structure
    from core.tasks import process_file_task
    
    for file_path in files:
        # Pass absolute string path to Celery task
        process_file_task.delay(str(file_path.resolve()), request.user.id)
        
    return JsonResponse({'message': f'Processing started for {len(files)} files'})
