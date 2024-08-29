from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User as CustomUser
from .models import UserAvatar, AvatarGroup


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
                    "fcm_key",
                    "color",
                    "gender",
                ),
            },
        ),
    )


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    fields = ["title","product_id","avatar_group", "image_url", "color", "paid" ]
    list_display = ("id", "title","product_id","avatar_group", "image_url", "color", "paid")



@admin.register(AvatarGroup)
class AvatarGroupAdmin(admin.ModelAdmin):
    fields = ["name","product_id" ]
    list_display = ("id", "name", "product_id")
