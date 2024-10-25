from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import (
    HabitGroup,
    Habit,
    HabitHistory,
    HabitProgress,
    Icon,
    RoutineTask,
    HabitTemplate,
    LifeSpheres,
    TemplateBundles,
    TemplateBundlesTranslation,
    HabitTemplateTranslation,
)

from rest_framework.exceptions import ValidationError


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    fields = [
        "user",
        "name",
        "description",
        "made_from",
        "goal",
        "habit_type",
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
        "description",
        "goal",
        "made_from",
        "habit_type",
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


@admin.register(RoutineTask)
class RoutineTaskAdmin(admin.ModelAdmin):
    fields = ["habit", "name", "is_done"]
    list_display = ("id", "habit", "name", "is_done")


@admin.register(HabitTemplate)
class HabitTemplateAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "description",
        "short_description",
        "routine_tasks",
        "goal",
        "habit_group",
        "habit_type",
        "repeat_period",
        "icon",
        "track_time",
        "due_dates",
        "text_is_ai_generated",
        "paid",
        "active",
    ]
    list_display = (
        "id",
        "name",
        "description",
        "short_description",
        "routine_tasks",
        "goal",
        "habit_group",
        "habit_type",
        "repeat_period",
        "icon",
        "track_time",
        "due_dates",
        "text_is_ai_generated",
        "paid",
        "active",
    )


@admin.register(HabitGroup)
class HabitGroupAdmin(admin.ModelAdmin):
    fields = ["name", "color", "product_id", "paid"]
    list_display = ("id", "name", "color", "product_id", "paid")


@admin.register(HabitProgress)
class HabitProgressAdmin(admin.ModelAdmin):
    fields = ["user", "habit", "current_value"]
    list_display = ("id", "habit", "current_value", "current_goal", "update_time")


@admin.register(HabitHistory)
class HabitHistoryAdmin(admin.ModelAdmin):
    fields = ["user", "habit", "date", "status"]
    list_display = ("user", "habit", "date", "status")


@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    fields = ["name", "emoji_name", "habit_group", "paid"]
    list_display = ("id", "name", "emoji_name", "habit_group", "paid")


@admin.register(HabitTemplateTranslation)
class HabitTemplateTranslationAdmin(admin.ModelAdmin):
    list_display = ("habit_template", "language_code", "name")
    list_filter = ("language_code",)
    search_fields = ("habit_template__name", "name")


@admin.register(LifeSpheres)
class LifeSpheresAdmin(admin.ModelAdmin):
    fields = ["name", "habit_groups"]
    list_display = ("id", "name")
    filter_horizontal = ("habit_groups",)


class TemplateBundlesTranslationInline(admin.TabularInline):
    model = TemplateBundlesTranslation
    extra = 1  # Количество пустых полей для новых переводов


class TemplateBundlesAdmin(admin.ModelAdmin):
    inlines = [TemplateBundlesTranslationInline]
    filter_horizontal = ("templates", "sub_bundles", "life_spheres")
    list_display = ["id", "name", "description"]
    search_fields = ["name"]

    def save_model(self, request, obj, form, change):
        """
        Проверка циклической зависимости перед сохранением модели.
        """
        if obj.has_cyclic_dependency():
            raise ValidationError(
                "Cyclic dependency detected: a bundle cannot reference itself directly or indirectly."
            )
        super().save_model(request, obj, form, change)


admin.site.register(TemplateBundles, TemplateBundlesAdmin)
admin.site.register(TemplateBundlesTranslation)
