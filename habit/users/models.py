import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .utils import user_directory_path


class User(AbstractUser, PermissionsMixin):
    """
    User Profile
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        verbose_name="Фото_профиля",
    )

    def __str__(self):
        return self.username
