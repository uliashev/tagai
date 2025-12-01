from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class GeminiSettingsForm(forms.ModelForm):
    gemini_api_key = forms.CharField(
        label="Gemini API-KEY",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Gemini API Key'})
    )
    gemini_model = forms.CharField(
        label="LLM model",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter LLM Model'})
    )
    gemini_prompt = forms.CharField(
        label="Gemini Prompt",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Gemini Prompt', 'rows': 3})
    )

    class Meta:
        model = User
        fields = ['gemini_api_key', 'gemini_model', 'gemini_prompt']

class OpenAISettingsForm(forms.ModelForm):
    openai_api_key = forms.CharField(
        label="Openai API-KEY",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Openai API Key'})
    )
    openai_model = forms.CharField(
        label="LLM model",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter LLM Model'})
    )
    openai_prompt = forms.CharField(
        label="Openai Prompt",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Openai Prompt', 'rows': 3})
    )

    class Meta:
        model = User
        fields = ['openai_api_key', 'openai_model', 'openai_prompt']
