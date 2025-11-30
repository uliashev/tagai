from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for Tagai.
    Currently identical to AbstractUser but allows for future extension.
    """
    gemini_api_key = models.CharField(max_length=255, blank=True, null=True, verbose_name="Gemini API Key")
