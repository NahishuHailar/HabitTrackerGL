from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import HabitGroup, Habit, HabitHistory, HabitProgress, Icon


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    fields = [
        "user",
        "name",
        "goal",
        "current_value",
        "habit_group",
        "status",
        "repeat_period",
        "icon",
        "track_time",
        "due_dates",
    ]
    list_display = (
        "id",
        "user",
        "name",
        "goal",
        "current_value",
        "habit_group",
        "status",
        "repeat_period",
        "icon",
        "track_time",
        "due_dates",
        "start_day",
        "update_time",
    )


@admin.register(HabitGroup)
class HabitGroupAdmin(admin.ModelAdmin):
    fields = ["name", "color", "product_id", "paid"]
    list_display = ("id", "name", "color", "product_id", "paid")


@admin.register(HabitProgress)
class HabitProgressAdmin(admin.ModelAdmin):
    fields = ["user", "habit", "current_value"]
    list_display = ("id", "habit", "current_value", "update_time")


@admin.register(HabitHistory)
class HabitHistoryAdmin(admin.ModelAdmin):
    fields = ["user", "habit", "date", "status"]
    list_display = ("user", "habit", "date", "status")


@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    fields = ["name", "emoji_name", "habit_group", "paid"]
    list_display = ("id", "name", "emoji_name", "habit_group", "paid")
