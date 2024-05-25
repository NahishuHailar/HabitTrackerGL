from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import HabitGroup, Habit, HabitProgress


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    fields = ["user", "name", "goal", "current_value", "habit_group", "progress_status",
        "repeat_period",]
    list_display = (
        "id",
        "user",
        "name",
        "goal",
        "current_value",
        "habit_group",
        "progress_status",
        "repeat_period",
    )


@admin.register(HabitGroup)
class HabitGroupAdmin(admin.ModelAdmin):
    fields = [
        "name",
    ]
    list_display = (
        "id",
        "name",
    )


@admin.register(HabitProgress)
class HabitProgressAdmin(admin.ModelAdmin):
    fields = ["user", "habit", "current_value"]
    list_display = ("id", "habit", "current_value", "update_time")
