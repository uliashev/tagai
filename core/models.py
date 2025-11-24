from django.db import models
import uuid


class BaseModel(models.Model):
    """
    An abstract base model that provides common fields for all models in the application.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)
