from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ["username", "phone", "image", "password", "email"]
    list_display = (
        "id",
        "username",
        "phone",
        "image",
    )
    ordering = ("email",)
