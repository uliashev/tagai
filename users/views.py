from django.contrib.auth.views import LoginView
from .forms import UserLoginForm

class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

def home(request):
    from django.shortcuts import render
    return render(request, 'users/home.html')
