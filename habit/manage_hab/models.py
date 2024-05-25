from django.db import models
from users.models import User


class Habit(models.Model):
    """
    Сurrent user's habit.
    """

    # Habit status Choices
    PROGRESSSTATUS = (
        ("ac", "active"),
        ("ar", "archive"),
        ("dn", "done"),
        ("dl", "deleted"),
        ("no", "None"),
    )
    REPEATPERIOD = (
        ("da", "day"),
        ("we", "week"),
        ("mo", "month"),
        ("ye", "year"),
        ("al", "always"),
    )

    user = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Пользователь"
    )
    habit_group = models.ForeignKey(
        "HabitGroup",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        verbose_name="Группа привычки",
    )
    name = models.CharField(max_length=300, verbose_name="Название привычки")
    goal = models.SmallIntegerField(verbose_name="Цель")
    current_value = models.SmallIntegerField(verbose_name="Текущее значение")
    progress_status = models.CharField(
        max_length=20, choices=PROGRESSSTATUS, verbose_name="Статус выполнения", default="ac"
    )
    repeat_period = models.CharField(
        max_length=20, choices=REPEATPERIOD, verbose_name="Период повтора", default="al"
    )

    def __str__(self):
        return self.name


class HabitProgress(models.Model):
    """
    habit progress history
    """

    habit = models.ForeignKey(
        Habit, on_delete=models.PROTECT, verbose_name="Привычка"
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Пользователь"
    )
    current_value = models.SmallIntegerField(verbose_name="Текущее значение")
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + self.habit.name


class HabitGroup(models.Model):
    """
    habit group. A habit may not have a group
    """

    name = models.CharField(max_length=300, verbose_name="Название группы")

    def __str__(self):
        return self.name
