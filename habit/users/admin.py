from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User as CustomUser
from .models import UserAvatar


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "auth_type",
        "firebase_key",
        "avatar",
        "image",
        "color",
        "gender",


    )
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Custom Fields",
            {
                "fields": (
                    "phone",
                    "image",
                    "avatar",
                    "auth_type",
                    "firebase_key",
                    "color",
                    "gender",
                ),
            },
        ),
    )


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    fields = ["title", "image_url", "color" ]
    list_display = ("id", "title", "image_url", "color")