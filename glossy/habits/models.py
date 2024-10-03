from tabnanny import check
from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User
from habits.services.constants import PROGRESSSTATUS, REPEATPERIOD, TRACKTIME, COLOR, HABITTYPE
from api.v1.services.manager import ActiveHabitManager


class Habit(models.Model):
    """
    Сurrent user's habit.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User", db_index=True,
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
    name = models.CharField(max_length=50, verbose_name="Habit name", blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True) 
    goal = models.SmallIntegerField(verbose_name="Goal", blank=True, null=True)
    current_value = models.SmallIntegerField(verbose_name="Current value", blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=PROGRESSSTATUS, verbose_name="Habit status", default="active"
    )
    repeat_period = models.CharField(
        max_length=20, choices=REPEATPERIOD, verbose_name="Repeat period", default="always"
    )    
    icon = models.CharField(max_length=20, verbose_name="Icon", blank=True, null=True)
    track_time = models.CharField(    # For a daily habit (morning, noon, evening)
        max_length=20,
        choices=TRACKTIME,
        verbose_name="Track time", 
        default="all_day",
    )
    due_dates = ArrayField(    # For habits with a repeat period of a week/month/year
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

    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, verbose_name="Habit"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User"
    )
    current_value = models.SmallIntegerField(verbose_name="Current value")
    # if habit.repeat_period == "always" - current_goal=Null
    current_goal = models.SmallIntegerField(verbose_name="Current goal", null=True, blank=True)
    # For habits with a repeat period of a week/month/year
    current_due_dates = ArrayField(    
        models.CharField(),
        null=True,
        blank=True,
        verbose_name="Current Due dates" 
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
        max_length=20,
        choices=COLOR,
        default="green",
        verbose_name="Group's color"
    )
    product_id = models.CharField(max_length=100, verbose_name="product id", default="_")
    paid = models.BooleanField(verbose_name="Paid", default=False)


    def __str__(self):
        return self.name


class Icon(models.Model):
    """
    list of icons app.
    """

    name = models.CharField(
        max_length=50, verbose_name="Title", db_index=True
    )
    emoji_name = models.CharField(
        max_length=50, verbose_name="Emoji title",
    ) 
    habit_group = models.ForeignKey(
        HabitGroup,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        verbose_name="Habit group",
    )
    paid = models.BooleanField(verbose_name='Paid', default=False)

    def __str__(self):
        return self.name
    