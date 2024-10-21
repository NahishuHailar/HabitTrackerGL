"""
Formation of habit calendars.
Separately for each type of habit (status).
A shared calendar that includes progress on all user habits (combines all user calendars).
"""
from collections import defaultdict
from datetime import datetime

from habits.models import Habit
from .old_daily_calendar import get_old_daily_habit_progress
from .old_weekly_calendar import get_old_weekly_habit_progress
from .old_mothly_calendar import get_old_monthly_habit_progress
from .old_annual_calendar import get_old_yearly_habit_progress
from .old_always_calendar import get_old_always_habit_progress

def get_old_progress_calendar(user_id, habit_id):
    """
    Get progress by habit depending on the type of habit.
    Daily/Weekly/Monthly/Annual/Always
    """
    habit = Habit.objects.get(user_id=user_id, id=habit_id)
    start_day = habit.start_day.replace(tzinfo=None).date()
    end_day = datetime.today().date()
    if habit.repeat_period == 'day':
        return get_old_daily_habit_progress(user_id, habit_id, start_day, end_day)
    elif habit.repeat_period == 'week':
        return get_old_weekly_habit_progress(user_id, habit_id, start_day, end_day)
    elif habit.repeat_period == 'month':
        return get_old_monthly_habit_progress(user_id, habit_id, start_day, end_day)
    elif habit.repeat_period == 'year':
        return get_old_yearly_habit_progress(user_id, habit_id, start_day, end_day)
    elif habit.repeat_period == 'always':
        return get_old_always_habit_progress(user_id, habit_id, start_day, end_day)
    else:
        return {}


def get_old_common_progress_calendar(user_id):
    """
    Overall result for each habit for each day.
    For every day: habits: ['green', 'green', 'green'] --> green (all - green)
                   habits: ['green', 'yellow', 'yellow'] --> yellow (any - yellow)
                   habits: ['yellow', 'yellow', 'yellow'] --> yellow (all - yellow)
    """
    # A list of all the user's active habits
    habit_list = Habit.active.filter(user=user_id)
    all_calendars = []
    
    # Summary list of results for each individual active habit
    for habit in habit_list:
        all_calendars.append(get_old_progress_calendar(user_id=user_id, habit_id=habit.id))
        
    combined_values = defaultdict(list)
    for habit_calendar in all_calendars:
            for date, color in habit_calendar.items():
                combined_values[date].append(color)

    common_calendar = {}
    # Calculating the result for each day
    for date, colors in combined_values.items():
        if all(color == 'green' for color in colors):
            common_calendar[date] = 'green'
        else:
            common_calendar[date] = 'yellow'
           
    return dict(sorted(common_calendar.items()))




