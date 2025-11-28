from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model for Tagai.
    Currently identical to AbstractUser but allows for future extension.
    """
    pass
