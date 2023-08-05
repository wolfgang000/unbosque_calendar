from django.urls import path
from . import views


urlpatterns = [
    path("accounts/oauth/google_authorize_url/", views.get_authorization_url),
    path("accounts/oauth/google_callback/", views.google_callback),
]
