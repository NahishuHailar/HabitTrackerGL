"""
Creating a calendar for a habit with year repeat period 
"""

from collections import defaultdict
from datetime import timedelta

from django.db.models import Max

from manage_hab.models import HabitProgress, Habit
from manage_hab.services.due_dates import get_numbers_of_due_dates


def get_yearly_habit_progress(user_id, habit_id, start_day, end_day):
    """
    We work separately with each reporting year of a given period.
    For each yaer :
    Trekking days are green (dot on the calendar)
    Deadline days : yellow (dot on the calendar)
    If the tracking day appears, then we delete the nearest deadline 
    day of the current year
    """
    habit = Habit.objects.get(id=habit_id, user_id=user_id)
    
    # Creating a list of years for the reporting period
    year_periods = get_year_periods(start_day, end_day)
    # Get the ordinal numbers of the days of the yaer for deadlines
    numbers_due_dates = get_numbers_of_due_dates(habit.due_dates, period="year")
    result = defaultdict(str)
    
    # Get a list of all the trekking for the entire period
    all_progress = HabitProgress.objects.filter(
        user_id=user_id,
        habit_id=habit_id,
        update_time__range=[start_day, end_day]
    ).values('update_time').annotate(max_value=Max('current_value'))

    progress_by_year = defaultdict(list)
    #Converting tracking habit data into a dictionary
    # {(start_year, end_year): [habit.trekking_day_1, habit.trekking_day_1]}
    # example {("2024-01-01", "2024-12-31"): ["2024-07-02", "2024-10-05"]}
    for entry in all_progress:
        update_time = entry['update_time']
        start_of_year = update_time.replace(month=1, day=1)
        end_of_year = start_of_year.replace(month=12, day=31)
        progress_by_year[(start_of_year, end_of_year)].append(update_time)

    # iteration for each reporting year
    for start_year, end_year in year_periods:
        progress_dates = progress_by_year[(start_year, end_year)]

        # Creating a list of deadlines for the current year
        year_due_dates = [(start_year + timedelta(days=n)).strftime('%Y-%m-%d') for n in numbers_due_dates]

        # Deleting the nearest deadline for each tracking habit
        for date in progress_dates:
            result[date.strftime('%Y-%m-%d')] = 'green'
            if year_due_dates:
                year_due_dates.pop(0)
        
        # The remaining deadlines are marked as yellow
        for date in year_due_dates:
            if date not in result:
                result[date] = 'yellow'

    sorted_result = sorted(result.items())
    return [{date: color} for date, color in sorted_result]


def get_year_periods(start_day, end_day):
    """
    The periods are divided into years.
    The beginning of the first period is the first day of the habit start year.
    The end of the last period is the last day of the current year
    """
    years = []
    current_start = start_day.replace(month=1, day=1)
    current_end = current_start.replace(month=12, day=31)

    while current_end <= end_day:
        years.append((current_start, current_end))
        current_start = current_start.replace(year=current_start.year + 1, month=1, day=1)
        current_end = current_start.replace(month=12, day=31)

    # Check if the last period does not fully cover a year, add it
    if current_start <= end_day:
        years.append((current_start, current_end))

    return years