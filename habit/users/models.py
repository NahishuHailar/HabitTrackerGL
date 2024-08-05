import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .constants import AUTHTYPE, GENDER
from manage_hab.constants import COLOR
from .utils import user_directory_path # ЗАГРУЗКА ПОЛЬЗОВАТЕЛЬСКОГО ИЗОБРАЖЕНИЯ


class User(AbstractUser):
    """
    User Profile
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    firebase_key = models.CharField(max_length=32, blank=True, null=True)
    username = models.CharField( max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField()
    phone = models.PositiveIntegerField(blank=True, null=True)
    image = models.CharField(
        verbose_name="Profile_photo",
        max_length=300,
        blank=True,
        null=True,
    )
    avatar = models.ForeignKey(
        "UserAvatar",
        on_delete=models.PROTECT,
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
    color = models.CharField(
        max_length=20,
        choices=COLOR,
        null=True,
        blank=True,
        default="green",
       )

    gender = models.CharField(
        max_length=20,
        choices=GENDER,
        null=True,
        blank=True

    )

    def __str__(self):
        return self.username

class UserAvatar(models.Model):
    """
    Users avatar
    """

    title = models.CharField(max_length=300, verbose_name="Название", db_index=True)
    image_url = models.URLField(max_length=200, verbose_name="url изображения")

    color = models.CharField(
        max_length=20,
        choices=COLOR,
        default="green",
        verbose_name="Цвет аватара"
    )

    def __str__(self):
        return self.title