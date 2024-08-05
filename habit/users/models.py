import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

<<<<<<< Updated upstream
from .utils import user_directory_path
=======
from .constants import AUTHTYPE, GENDER
from manage_hab.constants import COLOR
from .utils import user_directory_path # ЗАГРУЗКА ПОЛЬЗОВАТЕЛЬСКОГО ИЗОБРАЖЕНИЯ
>>>>>>> Stashed changes


class User(AbstractUser):
    """
    User Profile
    """
<<<<<<< Updated upstream

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
=======
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
>>>>>>> Stashed changes
        blank=True,
        null=True,
        verbose_name="Фото_профиля",
    )
    auth_type = models.CharField(
        max_length=20,
        choices=AUTHTYPE,
        verbose_name="Тип авторизации",
        default="none",
<<<<<<< Updated upstream
=======
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

>>>>>>> Stashed changes
    )

    def __str__(self):
        return self.username
