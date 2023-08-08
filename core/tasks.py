from celery import shared_task
from datetime import date, timedelta


def get_current_week_start_end():
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return (start, end)


@shared_task()
def update_user_schedule(user_id):
    print("hello")
