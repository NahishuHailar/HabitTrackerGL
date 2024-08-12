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
    habits = Habit.active.filter(user_id=user_id)
    
    for habit in habits:
        # Daily reset
        if habit.repeat_period == "day":
            if habit.update_time + timedelta(days=1) <= local_time:
                reset_current_value(habit)
        # Weekly reset
        elif habit.repeat_period == "week":
            if habit.update_time.isocalendar()[1] != local_time.isocalendar()[1]:
                reset_current_value(habit)
        # Monthly reset        
        elif habit.repeat_period == "month":
            if habit.update_time.month != local_time.month or habit.update_time.year != local_time.year:
                reset_current_value(habit)
        # Annual reset
        elif habit.repeat_period == "year":
            if habit.update_time.year != local_time.year:
               reset_current_value(habit)


def reset_current_value(habit):
    """
    Reset the current value of a habit to 0 and save the habit.
    """
    habit.current_value = 0
    habit.save()
