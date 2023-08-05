from django.shortcuts import render
from django.http import HttpResponseRedirect
from httpx import Client
from oauthlib.oauth2 import WebApplicationClient
from result import Err, Ok, Result
from django.conf import settings

class GoogleOAuth:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        token_uri: str = "https://oauth2.googleapis.com/token",
        authorize_url: str = "https://accounts.google.com/o/oauth2/auth",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_uri = token_uri
        self.authorize_url = authorize_url
        self.client = WebApplicationClient(client_id)

    def get_authorization_url(self):
        return self.client.prepare_request_uri(
            self.authorize_url,
            redirect_uri=self.redirect_uri,
            scope=["https://www.googleapis.com/auth/calendar.app.created"],
            access_type="offline", 
            prompt="select_account"
        )

    def fetch_token(self, code) -> Result[dict, str]:
        body = self.client.prepare_request_body(
            code=code, redirect_uri=self.redirect_uri, client_secret=self.client_secret,
        )
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        with Client() as client:
            result = client.post(
                self.token_uri,
                content=body,
                headers=headers,
            )
            if result.status_code == 200:
                return Ok(result.json())
            else:
                return Err(result.text)


client = GoogleOAuth(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    redirect_uri=settings.GOOGLE_REDIRECT_URI,
)

def get_authorization_url(request):
    redirect_url =  client.get_authorization_url()
    return HttpResponseRedirect(redirect_url)


def google_callback(request):
    code = request.GET.get("code")
    fetch_token_result = client.fetch_token(code)
    if isinstance(fetch_token_result, Err):
        pass

    token = fetch_token_result.unwrap()
    access_token = token["access_token"]
    refresh_token = token["refresh_token"]
    return HttpResponseRedirect("")

