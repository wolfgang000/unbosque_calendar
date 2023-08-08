from celery import shared_task
from datetime import date, timedelta
from django.conf import settings
import google.auth.transport.requests
from core import api, models
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_current_week_start_end():
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return (start, end)


@shared_task()
def update_user_schedule(user_id):
    user = models.User.objects.get(id=user_id)
    creds = Credentials(
        "",
        refresh_token=user.refresh_token,
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token",
    )
    request = google.auth.transport.requests.Request()
    creds.refresh(request)
    service = build("calendar", "v3", credentials=creds)
    # events = service.events().list(calendarId=created_calendar['id'], timeMax="", timeMin="2024-06-03T10:00:00-07:00").execute()
    today = date.today()
    table = api.get_student_schedule_table_html(user.doc_id, str(today), str(today))
    parsed_table = api.parse_table(table)
