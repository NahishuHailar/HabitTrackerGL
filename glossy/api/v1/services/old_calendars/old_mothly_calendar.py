"""
Creating a calendar for a monthlly habit
"""

from collections import defaultdict
from datetime import datetime, timedelta
from calendar import monthrange

from django.db.models import Max

from habits.models import HabitProgress, Habit
from api.v1.services.old_calendars.old_due_dates import get_numbers_of_due_dates




def get_old_monthly_habit_progress(user_id, habit_id, start_day, end_day):
    """
    We work separately with each reporting month of a given period.
    For each week :
    Trekking days are green (dot on the calendar)
    Deadline days : yellow (dot on the calendar)
    If the tracking day appears, then we delete the nearest deadline 
    day of the current month
    """
    habit = Habit.objects.get(id=habit_id, user_id=user_id)


    month_periods = get_month_periods(start_day, end_day)
    # Get the ordinal numbers of the days of the month for deadlines
    numbers_due_dates = get_numbers_of_due_dates(habit.due_dates, period='month')

    result = defaultdict(str)
    # Get a list of all the trekking for the entire period
    all_progress = HabitProgress.objects.filter(
        user_id=user_id,
        habit_id=habit_id,
        update_time__range=[start_day, end_day]
    ).values('update_time').annotate(max_value=Max('current_value'))

    progress_by_month = defaultdict(list)
    #Converting tracking habit data into a dictionary
    #{(start_month, end_month): [habit.trekking_day_1, habit.trekking_day_1]}
    # example {("2024-07-01", "2024-07-31"): ["2024-07-11", "2024-07-24"]}
    for entry in all_progress:
        update_time = entry['update_time']
        start_of_month = update_time.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=monthrange(start_of_month.year, start_of_month.month)[1] - 1))
        progress_by_month[(start_of_month, end_of_month)].append(update_time)

    # iteration for each reporting month
    for start_month, end_month in month_periods:
        progress_dates = progress_by_month[(start_month, end_month)]

        # Creating a list of deadlines for the current month
        month_due_dates = [start_month + timedelta(days=n) for n in numbers_due_dates]

        # Deleting the nearest deadline for each tracking habit
        for date in progress_dates:
            result[date] = 'green'
            if month_due_dates:
                month_due_dates.pop(0)

        # The remaining deadlines are marked as yellow
        for date in month_due_dates:
            if date not in result:
                result[date] = 'yellow'

    result = {
        datetime.strftime(key, '%Y-%m-%d'): value 
        for key, value in sorted(result.items()) if key >= start_day
        }
    return result


def get_month_periods(start_day, end_day):
    """
    The periods are divided into months.
    The beginning of the first period is the first day of the habit start month.
    The end of the last period is the last day of the current month
    """
 
    months = []
    current_start = start_day.replace(day=1)
    current_end = (current_start + timedelta(days=monthrange(current_start.year, current_start.month)[1] - 1))
    while current_end <= end_day:
        months.append((current_start, current_end))
        if current_start.month == 12:
            current_start = current_start.replace(year=current_start.year + 1, month=1, day=1)
        else:
            current_start = current_start.replace(month=current_start.month + 1, day=1)
        current_end = (current_start + timedelta(days=monthrange(current_start.year, current_start.month)[1] - 1))

    # Check if the last period does not fully cover a month, add it
    if current_start <= end_day:
        months.append((current_start, current_end))

    return months


