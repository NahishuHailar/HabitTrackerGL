"""
Creating a calendar for a daily habit.
Get daily habit progress based on pagination parameter.
pagination == 0: current month
pagination == 1: previous month
pagination == 2: two months ago, etc.
"""

from django.db.models import Max, F
from habits.models import HabitProgress
from .month_range import get_month_range


def get_daily_habit_progress(user_id, habit_id, start_day, end_day, pagination=1):
    """
    The habit is fully fulfilled - green (number of executions >= daily goal).
    The habit is partially fulfilled - yellow  (0 <number of executions < daily goal)
    The habit is not fulfilled - we do not return anything (number of executions == 0)

    """
    # Determine the date of the first and last day of the month based on pagination
    first_day_of_month, last_day_of_month = get_month_range(end_day, pagination)

    # If the month specified in the pagination coincides with the month of the habit start,
    # check that the start date is not earlier than the start of the habit

    if (
        start_day.year == first_day_of_month.year
        and start_day.month == first_day_of_month.month
    ):
        if start_day > first_day_of_month:
            first_day_of_month = start_day

    # If this is the current month, we limit the end date to today
    if last_day_of_month > end_day:
        last_day_of_month = end_day

    progress_records = (
        HabitProgress.objects.filter(
            user_id=user_id,
            habit_id=habit_id,
            update_time__range=[first_day_of_month, last_day_of_month],
        )
        .values("update_time")
        .annotate(max_value=Max("current_value"), goal=F("current_goal"))
    )

    progress_dict = {}
    for record in progress_records:
        date_str = record["update_time"].strftime("%Y-%m-%d")
        goal = record["goal"] or 1  # Default goal is 1 if None or 0
        if record["max_value"] >= goal:
            progress_dict[date_str] = "green"
        elif record["max_value"] > 0:
            progress_dict[date_str] = "yellow"

    result = dict(sorted(progress_dict.items()))
    return result
