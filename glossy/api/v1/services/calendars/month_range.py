from calendar import monthrange 
from dateutil.relativedelta import relativedelta
from datetime import timedelta


def get_month_range(current_date, pagination):
    """
    Calculate the first and last day of the month depending on the pagination.  
    """
    
    target_month = current_date.replace(day=1) - relativedelta(months=pagination)

    first_day_of_month = target_month.replace(day=1)
    last_day_of_month = target_month.replace(day=monthrange(target_month.year, target_month.month)[1])

    return first_day_of_month, last_day_of_month