"""Due_dates for all habit types(Habit.repeat_period)"""

from dateutil import parser


def get_numbers_of_due_dates(due_dates, period):
    """
    Returns the ordinal number of the deadline days
    depending on the period of repetition of the habit
    (0, 2, 4) == (Monday, Wednesday, Friday) period == "week"
    """
    result = []
    for date in due_dates:
        date_obj = parser.parse(date)
        if period == "week":
            result.append(date_obj.weekday())
        elif period == "month":
            result.append(date_obj.day - 1)
        elif period == "year":
            result.append(date_obj.timetuple().tm_yday - 1)
    result.sort()
    return tuple(result)
