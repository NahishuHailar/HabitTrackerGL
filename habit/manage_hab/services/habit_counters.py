"""
At the beginning of each new cycle of habit fulfillment (day/week/month/year), 
the Habit.current_value must be reset to zero
"""
from datetime import datetime, timedelta
from manage_hab.models import Habit

def reset_habits_counters(user_id, local_time_str):
    """
    Reset the counters of the current value of habits every new day, week, month, or year.
    """
    local_time = datetime.fromisoformat(local_time_str).date()
    habits = Habit.objects.filter(user_id=user_id, status="active")
    
    for habit in habits:
        if habit.repeat_period == "day":
            reset_habit(habit, local_time, timedelta(days=1))
        elif habit.repeat_period == "week":
            reset_habit(habit, local_time, timedelta(weeks=1))
        elif habit.repeat_period == "month":
            if habit.update_time.month != local_time.month or habit.update_time.year != local_time.year:
                habit.current_value = 0
                habit.save()
        elif habit.repeat_period == "year":
            if habit.update_time.year != local_time.year:
                habit.current_value = 0
                habit.save()

def reset_habit(habit, local_time, time_delta):
    if habit.update_time + time_delta <= local_time:
        habit.current_value = 0
        habit.save()

