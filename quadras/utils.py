from django.utils import timezone
from datetime import datetime, timedelta, time, date


def schedule_str_format(time_start, time_end, step_minutes=60):
    schedule_list = []

    current_datetime = datetime.combine(datetime.today(), time(hour=time_start))
    end_datetime = datetime.combine(datetime.today(), time(hour=time_end))

    while current_datetime < end_datetime:
        schedule_list.append(current_datetime.time())
        current_datetime += timedelta(minutes=step_minutes)
    
    return schedule_list


def session_current_week(current_date_day):
    days = []
    while len(days) < 7:
        days.append(current_date_day)
        current_date_day += timedelta(days=1)
    return days


def next_week(current_week_session):
    return current_week_session + timedelta(days=7)


def previous_week(current_week_session):
    return current_week_session - timedelta(days=7)