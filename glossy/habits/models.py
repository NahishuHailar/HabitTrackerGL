from enum import unique
from tabnanny import check
from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User
from habits.services.constants import (
    PROGRESSSTATUS,
    REPEATPERIOD,
    TRACKTIME,
    COLOR,
    HABITTYPE,
)
from api.v1.services.manager import ActiveHabitManager
from rest_framework.exceptions import ValidationError


class Habit(models.Model):
    """
    Сurrent user's habit.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        db_index=True,
    )
    habit_group = models.ForeignKey(
        "HabitGroup",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        verbose_name="Habit group",
    )
    habit_type = models.CharField(
        max_length=20, choices=HABITTYPE, verbose_name="Habit type", default="regular"
    )
    name = models.CharField(
        max_length=50, verbose_name="Habit name", blank=True, null=True
    )
    made_from = models.ForeignKey(
        "HabitTemplate",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        verbose_name="Parrent template",
    )
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    goal = models.SmallIntegerField(verbose_name="Goal", blank=True, null=True)
    current_value = models.SmallIntegerField(
        verbose_name="Current value", blank=True, null=True, default=0
    )
    status = models.CharField(
        max_length=20,
        choices=PROGRESSSTATUS,
        verbose_name="Habit status",
        default="active",
    )
    repeat_period = models.CharField(
        max_length=20,
        choices=REPEATPERIOD,
        verbose_name="Repeat period",
        default="always",
    )
    icon = models.CharField(max_length=20, verbose_name="Icon", blank=True, null=True)
    track_time = models.CharField(  # For a daily habit (morning, noon, evening)
        max_length=20,
        choices=TRACKTIME,
        verbose_name="Track time",
        default="all_day",
    )
    due_dates = ArrayField(  # For habits with a repeat period of a week/month/year
        models.CharField(),
        null=True,
        blank=True,
        verbose_name="Due dates",
    )
    start_day = models.DateTimeField(verbose_name="Start day", auto_now_add=True)
    update_time = models.DateField(verbose_name="Update time", auto_now=True)

    objects = models.Manager()  # The default manager
    active = ActiveHabitManager()  # Manager for only active habits

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['user', 'name'], name='unique_user_habit_name')
    #     ]

    def __str__(self):
        return self.name or "Habit Name isn't set"


class RoutineTask(models.Model):
    """
    Task for routine type habit.
    """

    habit = models.ForeignKey(
        "Habit",
        on_delete=models.CASCADE,
        related_name="routine_tasks",
        verbose_name="Habit",
    )
    name = models.CharField(max_length=100, verbose_name="Task name")
    is_done = models.BooleanField(default=False, verbose_name="Is Done")

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['habit', 'name'], name='unique_habit_task_name')
    #     ]

    def __str__(self):
        return f"{self.habit.name} - {self.name}"


class HabitProgress(models.Model):
    """
    Habit progress history
    """

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, verbose_name="Habit")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    current_value = models.SmallIntegerField(verbose_name="Current value")
    # if habit.repeat_period == "always" - current_goal=Null
    current_goal = models.SmallIntegerField(
        verbose_name="Current goal", null=True, blank=True
    )
    # For habits with a repeat period of a week/month/year
    current_due_dates = ArrayField(
        models.CharField(), null=True, blank=True, verbose_name="Current Due dates"
    )
    update_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username or "User name is'nt set" + self.habit.name


class HabitHistory(models.Model):
    """
    General activity history for each habit.
    Accounting for the total time of a habit in the active/archive status
    """

    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, verbose_name="Habit", db_index=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User", db_index=True
    )
    date = models.DateField(verbose_name="Date")
    status = models.CharField(
        max_length=20,
        choices=PROGRESSSTATUS,
        verbose_name="Habit Status",
        default="active",
    )

    def __str__(self):
        return f" {self.user.username} history of {self.habit.name}"


class HabitGroup(models.Model):
    """
    habit group. A habit may not have a group
    """

    name = models.CharField(max_length=300, verbose_name="Group name")
    color = models.CharField(
        max_length=20, choices=COLOR, default="green", verbose_name="Group's color"
    )
    product_id = models.CharField(
        max_length=100, verbose_name="product id", default="_"
    )
    paid = models.BooleanField(verbose_name="Paid", default=False)

    def __str__(self):
        return self.name


class Icon(models.Model):
    """
    list of icons app.
    """

    name = models.CharField(max_length=50, verbose_name="Title", db_index=True)
    emoji_name = models.CharField(
        max_length=50,
        verbose_name="Emoji title",
    )
    habit_group = models.ForeignKey(
        HabitGroup,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        verbose_name="Habit group",
    )
    paid = models.BooleanField(verbose_name="Paid", default=False)

    def __str__(self):
        return self.name


class HabitTemplate(models.Model):
    """
    Template for pre-defined habits.
    """

    name = models.CharField(max_length=50, verbose_name="Habit name", unique=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    short_description = models.TextField(
        verbose_name="Short description", blank=True, null=True
    )
    habit_group = models.ForeignKey(
        "HabitGroup",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        verbose_name="Habit group",
    )
    text_is_ai_generated = models.BooleanField(
        default=False, verbose_name="AI_Generated"
    )
    goal = models.SmallIntegerField(verbose_name="Goal", blank=True, null=True)
    habit_type = models.CharField(
        max_length=20, choices=HABITTYPE, verbose_name="Habit type", default="regular"
    )
    routine_tasks = ArrayField(
        models.CharField(),
        null=True,
        blank=True,
        verbose_name="Routine tasks",
    )
    repeat_period = models.CharField(
        max_length=20,
        choices=REPEATPERIOD,
        verbose_name="Repeat period",
        default="always",
    )
    icon = models.CharField(max_length=20, verbose_name="Icon", blank=True, null=True)
    track_time = models.CharField(
        max_length=20,
        choices=TRACKTIME,
        verbose_name="Track time",
        default="all_day",
    )
    due_dates = ArrayField(
        models.CharField(),
        null=True,
        blank=True,
        verbose_name="Due dates",
    )
    paid = models.BooleanField(verbose_name="Paid", default=False)
    copyDescription = models.BooleanField(verbose_name="CopyDescription", default=False)
    active = models.BooleanField(verbose_name="Active", default=True)

    def __str__(self):
        return self.name


class LifeSpheres(models.Model):
    """
    Spheres of human life balance wheel
    """

    name = models.CharField(max_length=300, verbose_name="Life_spheres_name")
    habit_groups = models.ManyToManyField(
        HabitGroup, blank=True, verbose_name="Habit groups"
    )

    def __str__(self):
        return self.name


class HabitTemplateTranslation(models.Model):
    """
    Translation for HabitTemplate.
    """

    habit_template = models.ForeignKey(
        "HabitTemplate",
        on_delete=models.CASCADE,
        related_name="translations",
        verbose_name="Habit template",
    )
    language_code = models.CharField(max_length=10, verbose_name="Language code")
    name = models.CharField(max_length=50, verbose_name="Habit name")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    short_description = models.TextField(
        verbose_name="Short description", blank=True, null=True
    )

    class Meta:
        unique_together = ("habit_template", "language_code")

    def __str__(self):
        return f"{self.habit_template.name} ({self.language_code})"


class TemplateBundles(models.Model):
    """
    Template bundles: a bundle can contain either habit templates or other bundles (recursive).
    """

    name = models.CharField(max_length=300, verbose_name="Template bundle name")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    templates = models.ManyToManyField(
        "HabitTemplate",
        related_name="template_bundles",
        blank=True,
        verbose_name="Habit templates",
    )
    sub_bundles = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="parent_bundles",
        verbose_name="Sub-bundles",
    )
    life_spheres = models.ManyToManyField(
        "LifeSpheres",
        related_name="template_bundles",
        blank=True,
        verbose_name="Life Spheres",
    )

    def clean(self):
        """
        Prevent cyclic dependencies by checking if a bundle references itself directly or indirectly.
        """
        if self.pk and self.has_cyclic_dependency():
            raise ValidationError(
                "Cyclic dependency detected: a bundle cannot reference itself directly or indirectly."
            )
        super().clean()

    def has_cyclic_dependency(self, visited=None):
        """
        Проверяет циклические зависимости. Если объект не сохранен (без pk),
        временно пропускаем его проверку в этом вызове.
        """
        # Если объект не сохранён, значит, его ещё нельзя проверить
        if not self.pk:
            return False

        visited = visited or set()
        if self in visited:
            return True

        visited.add(self)
        for sub_bundle in self.sub_bundles.all():
            if sub_bundle.has_cyclic_dependency(visited):
                return True

        return False

    def __str__(self):
        return self.name


class TemplateBundlesTranslation(models.Model):
    """
    Translation for TemplateBundles.
    """

    template_bundle = models.ForeignKey(
        TemplateBundles,
        on_delete=models.CASCADE,
        related_name="translations",
        verbose_name="Template bundle",
    )
    language_code = models.CharField(max_length=10, verbose_name="Language code")
    name = models.CharField(max_length=300, verbose_name="Translated name")
    description = models.TextField(
        verbose_name="Translated description", blank=True, null=True
    )

    class Meta:
        unique_together = ("template_bundle", "language_code")

    def __str__(self):
        return f"{self.template_bundle.name} ({self.language_code})"
