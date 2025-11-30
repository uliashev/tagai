from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class SettingsForm(forms.ModelForm):
    gemini_api_key = forms.CharField(
        label="Gemini",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Gemini API Key'})
    )

    class Meta:
        model = User
        fields = ['gemini_api_key']
