import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .utils import user_directory_path


class User(AbstractUser):
    """
    User Profile
    """

    AUTHTYPE = (
        ("google", "google"),
        ("apple", "apple"),
        ("none", "none"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        ("username"),
        max_length=150,
        unique=False,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        blank=True,
    )
    email = models.EmailField(verbose_name="email address", unique=True)
    phone = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        verbose_name="Фото_профиля",
    )
    auth_type = models.CharField(
        max_length=20,
        choices=AUTHTYPE,
        verbose_name="Тип авторизации",
        default="none",
    )

    def __str__(self):
        return self.username
