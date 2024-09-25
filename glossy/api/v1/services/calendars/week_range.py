from datetime import timedelta

def get_week_range(current_date, pagination):
    """
    Calculate the first and last day of the week depending on the pagination.
    """
    # Определяем начало недели (понедельник) для текущей даты
    start_of_current_week = current_date - timedelta(days=current_date.weekday())
    
    # Смещаем на нужное количество недель в зависимости от пагинации
    target_week_start = start_of_current_week - timedelta(weeks=pagination)
    
    # Определяем конец недели (воскресенье)
    target_week_end = target_week_start + timedelta(days=6)
    
    return target_week_start, target_week_end   