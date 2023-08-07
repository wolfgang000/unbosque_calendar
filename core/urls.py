from django.urls import path
from . import views


urlpatterns = [
    path("accounts/oauth/google_authorize_url/", views.get_authorization_url),
    path("accounts/oauth/google_callback/", views.google_callback),
    path("fetch_schedule/", views.fetch_schedule, name="fetch_schedule"),
    path(
        "subscribe_schedule_to_calendar/",
        views.subscribe_schedule_to_calendar,
        name="subscribe_schedule_to_calendar",
    ),
]
