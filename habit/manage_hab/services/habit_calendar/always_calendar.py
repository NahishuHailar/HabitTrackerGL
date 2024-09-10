"""
Creating a calendar for a "always" habit.
Get 'always' habit progress based on pagination parameter.
pagination == 0: current month
pagination == 1: previous month
pagination == 2: two months ago, etc.
"""
from django.db.models import Max

from manage_hab.models import HabitProgress
from manage_hab.services.month_range import get_month_range



def get_always_habit_progress(user_id, habit_id, start_day, end_day, pagination=0):
    """
    Every day of the trekking habit is marked with a green dot on the calendar.
    """
    # Determine the date of the first and last day of the month based on pagination
    first_day_of_month, last_day_of_month = get_month_range(end_day, pagination)
    
    #If the month specified in the pagination coincides with the month of the habit start,
    # check that the start date is not earlier than the start of the habit
    if start_day.year == first_day_of_month.year and start_day.month == first_day_of_month.month:
        if start_day > first_day_of_month:
            first_day_of_month = start_day

    # If this is the current month, we limit the end date to today
    if last_day_of_month > end_day:
        last_day_of_month = end_day       
    
    
    
    progress_records = HabitProgress.objects.filter(
        habit_id=habit_id,
        user_id=user_id,
        update_time__range=[first_day_of_month, last_day_of_month]
    ).values('update_time').annotate(max_value=Max('current_value'))
 
    result = {record['update_time'].strftime('%Y-%m-%d'): "green" for record in progress_records}
    return result