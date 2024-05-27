from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User as CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "auth_type",
    )
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Custom Fields",
            {
                "fields": (
                    "phone",
                    "image",
                    "auth_type",
                ),
            },
        ),
    )
