def chek_pagination(all_calendar):
    last_pages, out_of_ranges, all_calendars = [], [], []
    last_page, out_of_range = False, False

    for item in all_calendar:
        last_pages.append(item[1])
        out_of_ranges.append(item[2])
        all_calendars.append(item[0])

    if all(out_of_ranges):
        last_page, out_of_range = False, True
        return [], last_page, out_of_range
    
    if all(last_pages):
        last_page, out_of_range = True, False
        return all_calendars, last_page, out_of_range
    
    count_last_page, count_out_of_range = 0, 0
    for last_page in last_pages:
        if last_page:
            count_last_page += 1

    for out_of_range in out_of_ranges:
        if not out_of_range:
            count_out_of_range += 1

    if count_out_of_range == 1 and count_last_page == 1:
        last_page , out_of_range = True, False
        return all_calendars, last_page, out_of_range

    return all_calendars, last_page, out_of_range
