import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .constants import AUTHTYPE, AVATAR_GROUP, GENDER
from manage_hab.constants import COLOR
from .utils import user_directory_path  # ЗАГРУЗКА ПОЛЬЗОВАТЕЛЬСКОГО ИЗОБРАЖЕНИЯ


class User(AbstractUser):
    """
    User Profile
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    firebase_key = models.CharField(max_length=32, blank=True, null=True)
    fcm_key = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
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
        on_delete=models.CASCADE,
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

    gender = models.CharField(max_length=20, choices=GENDER, null=True, blank=True)

    def __str__(self):
        return self.username or "Name isn't set"


class UserAvatar(models.Model):
    """
    Users avatar
    """

    title = models.CharField(max_length=300, verbose_name="Название", db_index=True)
    product_id = models.CharField(max_length=100, verbose_name="product id", default="_")
    avatar_group = models.ForeignKey(
        "AvatarGroup",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Группа автара",
    )
    image_url = models.URLField(max_length=200, verbose_name="url изображения")

    color = models.CharField(
        max_length=20, choices=COLOR, default="green", verbose_name="Цвет аватара"
    )
    paid = models.BooleanField(verbose_name="Платная аватар", default=False)

    def __str__(self):
        return self.title


class AvatarGroup(models.Model):
    """
    Group of avatars.
    """
    name = models.CharField(
        max_length=50,
        choices=AVATAR_GROUP,
        verbose_name="Группа Аватара")
    product_id = models.CharField(
        max_length=100,
        verbose_name="product id",
        default="_",
        )

    def __str__(self):
        return self.name