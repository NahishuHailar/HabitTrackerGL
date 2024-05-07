from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
import uuid
from django.db import models

class User(AbstractUser, PermissionsMixin):
    """
    User Profile
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    
    def __str__(self):
        return self.username

