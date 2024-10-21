from calendar import monthrange 
from dateutil.relativedelta import relativedelta


def get_month_range(current_date, pagination, start_day):
    """
    Calculate the first and last day of the month depending on the pagination.  
    """
    
    target_month = current_date.replace(day=1) - relativedelta(months=pagination)

    start_month = start_day.replace(day=1)

    out_of_range = False

    if target_month < start_month:
        target_month = start_month
        out_of_range, last_page = True, False  
    else:
        last_page = target_month == start_month

    first_day_of_month = target_month.replace(day=1)
    last_day_of_month = target_month.replace(day=monthrange(target_month.year, target_month.month)[1])

    return first_day_of_month, last_day_of_month, last_page, out_of_range