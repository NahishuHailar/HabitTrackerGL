from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User
from .constants import PROGRESSSTATUS, REPEATPERIOD, TRACKTIME, COLOR
from .services.manager import ActiveHabitManager


class Habit(models.Model):
    """
    Сurrent user's habit.
    """
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Пользователь", db_index=True,
    )
    habit_group = models.ForeignKey(
        "HabitGroup",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        verbose_name="Группа привычки",
    )
    name = models.CharField(max_length=50, verbose_name="Название привычки", blank=True, null=True)
    goal = models.SmallIntegerField(verbose_name="Цель", blank=True, null=True)
    current_value = models.SmallIntegerField(verbose_name="Текущее значение", blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=PROGRESSSTATUS, verbose_name="Статус выполнения", default="active"
    )
    repeat_period = models.CharField(
        max_length=20, choices=REPEATPERIOD, verbose_name="Период повтора", default="always"
    )
    
    icon = models.CharField(max_length=20, verbose_name="Иконка", blank=True, null=True)
    track_time = models.CharField(    # For a daily habit (morning, noon, evening)
        max_length=20,
        choices=TRACKTIME,
        verbose_name="Время треккинга", 
        default="all_day",
    )
    due_dates = ArrayField(    # For habits with a repeat period of a week/month/year
        models.CharField(),
        null=True,
        blank=True,
        verbose_name="Сроки", 
    )
    start_day = models.DateTimeField(verbose_name="Дата начала", auto_now_add=True)

    update_time = models.DateField(verbose_name="Дата обновления", auto_now=True)

    objects = models.Manager()  # The default manager
    active = ActiveHabitManager()  # Manager for only active habits


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
    # if habit.repeat_period == "always" - current_goal=Null
    current_goal = models.SmallIntegerField(verbose_name="Цель", null=True, blank=True)
    # For habits with a repeat period of a week/month/year
    current_due_dates = ArrayField(    
        models.CharField(),
        null=True,
        blank=True,
        verbose_name="Сроки" 
    )
    update_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username + self.habit.name


class HabitHistory(models.Model):
    """
    General activity history for each habit.
    Accounting for the total time of a habit in the active/archive status
    """
    habit = models.ForeignKey(
        Habit, on_delete=models.PROTECT, verbose_name="Привычка", db_index=True
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Пользователь", db_index=True
    )
    date = models.DateField(verbose_name="Дата")
    status = models.CharField(
        max_length=20,
        choices=PROGRESSSTATUS,
        verbose_name="Статус выполнения",
        default="active",
    )

    def __str__(self):
        return f"История {self.user.username} {self.habit.name}"   


class HabitGroup(models.Model):
    """
    habit group. A habit may not have a group
    """

    name = models.CharField(max_length=300, verbose_name="Название группы")
    color = models.CharField(
        max_length=20,
        choices=COLOR,
        default="green",
        verbose_name="Цвет группы"
    )

    def __str__(self):
        return self.name


class Icon(models.Model):
    """
    list of icons app.
    """

    name = models.CharField(
        max_length=50, verbose_name="Название иконки", db_index=True
    )
    emoji_name = models.CharField(
        max_length=50, verbose_name="Название эмодзи",
    ) 
    habit_group = models.ForeignKey(
        HabitGroup,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        verbose_name="Группа привычки",
    )
    