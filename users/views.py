from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
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
