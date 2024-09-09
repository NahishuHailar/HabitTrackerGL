"""
Creating a calendar for a daily habit
"""
from datetime import timedelta

from django.db.models import Max, F
from manage_hab.models import HabitProgress

def get_daily_habit_progress(user_id, habit_id, start_day, end_day, pagination=1):
    """
    The habit is fully fulfilled - green (number of executions >= daily goal).
    The habit is partially fulfilled - yellow  (0 <number of executions < daily goal) 
    The habit is not fulfilled - we do not return anything (number of executions == 0)
    """
    # define the current week
    today = end_day
    current_week_start = today - timedelta(days=today.weekday())

    # Counting how many weeks you need to return    
    weeks_to_fetch = pagination + 1  # the coming week + previous ones
    start_date_to_return = current_week_start - timedelta(weeks=weeks_to_fetch)

    # do not return more data than starting from `Habit.start_day`
    if start_date_to_return < start_day:
        start_date_to_return = start_day


    # Get a list of all the trekking for the entire period
    progress_records = HabitProgress.objects.filter(
        user_id=user_id,
        habit_id=habit_id,
        update_time__range=[start_date_to_return, end_day]
    ).values('update_time').annotate(max_value=Max('current_value'), goal=F('current_goal'))
    
    progress_dict = {}
    for record in progress_records:
        date_str = record['update_time'].strftime('%Y-%m-%d')
        goal = record['goal'] or 1  # Default goal is 1 if None or 0
        if record['max_value'] >= goal:
            progress_dict[date_str] = "green"
        elif record['max_value'] > 0:
            progress_dict[date_str] = "yellow"

    result = dict(sorted(progress_dict.items()))
    return result
