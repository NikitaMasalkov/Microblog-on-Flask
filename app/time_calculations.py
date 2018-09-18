def total_time_spend(day):
    total_minutes = 0
    total_hours = 0
    for activity in day.activities:
        total_minutes += activity.minutes
        total_hours += activity.hours
    bonus_hours,total_minutes = divmod(total_minutes, 60)
    total_hours += bonus_hours
    day.total_minutes = total_minutes
    day.total_hours = total_hours
    return day

def overall_time(days, time):
    overall_minutes = 0
    overall_hours = 0
    for day in days:
        overall_hours += day.total_hours
        overall_minutes += day.total_minutes
    bonus_hours, overall_minutes = divmod(overall_minutes, 60)
    overall_hours += bonus_hours
    time.hours = overall_hours
    time.minutes = overall_minutes
    return time
