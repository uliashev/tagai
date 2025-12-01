from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for Tagai.
    Currently identical to AbstractUser but allows for future extension.
    """
    gemini_api_key = models.CharField(max_length=100, blank=True, null=True, verbose_name="Gemini API-KEY")
    gemini_model = models.CharField(max_length=50, blank=True, null=True, verbose_name="LLM model")
    gemini_prompt = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Gemini Prompt")
    openai_api_key = models.CharField(max_length=100, blank=True, null=True, verbose_name="Openai API-KEY")
    openai_model = models.CharField(max_length=50, blank=True, null=True, verbose_name="LLM model")
    openai_prompt = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Openai Prompt")
