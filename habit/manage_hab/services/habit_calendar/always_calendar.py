"""
Creating a calendar for a weekly habit
"""
from django.db.models import Max

from manage_hab.models import HabitProgress


def get_always_habit_progress(user_id, habit_id, start_day, end_day):
    """
    Every day of the trekking habit is marked with a green dot on the calendar.
    """
    progress_records = HabitProgress.objects.filter(
        habit_id=habit_id,
        user_id=user_id,
        update_time__range=[start_day, end_day]
    ).values('update_time').annotate(max_value=Max('current_value'))
 
    result = [{record['update_time'].strftime('%Y-%m-%d'): "green"} for record in progress_records]
    return result