"""
Creating a calendar for a weekly habit
"""

from collections import defaultdict
from datetime import  datetime, timedelta

from django.db.models import Max

from habits.models import HabitProgress, Habit
from .due_dates import get_numbers_of_due_dates
from .month_range import get_month_range




def get_weekly_habit_progress(user_id, habit_id, start_day, end_day, pagination=0):
    """
    We work separately with each reporting week of a given period.
    For each week :
    Trekking days are green (dot on the calendar)
    Deadline days : yellow (dot on the calendar)
    If the tracking day appears, then we delete the nearest deadline 
    day of the current week
    """
    habit = Habit.objects.get(id=habit_id, user_id=user_id)

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
   
    # Creating a list of weeks for the reporting period
    # Like [(start_week_1, end_week_1), (start_week_2, end_week_2) ...]
    week_periods = get_week_periods(first_day_of_month, last_day_of_month)

    # Get the ordinal numbers of the days of the week for deadlines
    # Like  (0, 2, 4) == (Monday, Wednesday, Friday) 
    numbers_due_dates = get_numbers_of_due_dates(habit.due_dates, period='week')
 
    result = defaultdict(str)

    # Get a list of all the trekking for the entire period
    all_progress = HabitProgress.objects.filter(
        user_id=user_id,
        habit_id=habit_id,
        update_time__range=[first_day_of_month, last_day_of_month]
    ).values('update_time').annotate(max_value=Max('current_value'))

    progress_by_week = defaultdict(list)
    #Converting tracking habit data into a dictionary
    # {(start_week, end_week): [habit.trekking_day_1, habit.trekking_day_1]}
    # example {("2024-07-01", "2024-07-07"): ["2024-07-02", "2024-07-05"]}
    for entry in all_progress:
        update_time = entry['update_time']
        start_of_week = update_time - timedelta(days=update_time.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        progress_by_week[(start_of_week, end_of_week)].append(update_time)

    # iteration for each reporting week
    for start_week, end_week in week_periods:
        progress_dates = progress_by_week[(start_week, end_week)]

        # Creating a list of deadlines for the current week
        week_due_dates = [start_week + timedelta(days=n) for n in numbers_due_dates]

        # Deleting the nearest deadline for each tracking habit
        for date in progress_dates:
            result[date] = 'green'
            if week_due_dates:
                week_due_dates.pop(0)

        # The remaining deadlines are marked as yellow
        for date in week_due_dates:
            if date not in result:
                result[date] = 'yellow'

    #Deleting the due_dates values before the start day of the habit
    result = {
        datetime.strftime(key, '%Y-%m-%d'): value 
        for key, value in sorted(result.items()) if key >= start_day
        }
    return result

def get_week_periods(start_day, end_day):
    """
    Getting a list of weekly periods from start_day to end_day.
    The last week is fully included
    """
    weeks = []
    current_start = start_day - timedelta(days=start_day.weekday())
    current_end = current_start + timedelta(days=6)

    # Only for habit.repeat_period =="week" :
    # added week period afteer current week (for new deadlines)
    # by end_day + timedelta(days=7)
    end_day = end_day + timedelta(days=7)
    while current_end <= end_day: 
        weeks.append((current_start, current_end))
        current_start += timedelta(days=7)
        current_end += timedelta(days=7)
    # Check if the last period does not fully cover a week, add it
    if current_start <= end_day:
        weeks.append((current_start, current_end))

    return weeks
