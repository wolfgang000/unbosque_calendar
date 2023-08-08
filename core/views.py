from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from httpx import Client
import httpx
from oauthlib.oauth2 import WebApplicationClient
from result import Err, Ok, Result
from django.conf import settings
from core import models
from core.forms import FetchScheduleForm, SubscribeScheduleToCalendarForm


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

    def get_authorization_url(self, state):
        return self.client.prepare_request_uri(
            self.authorize_url,
            redirect_uri=self.redirect_uri,
            scope=["https://www.googleapis.com/auth/calendar.app.created"],
            access_type="offline",
            prompt="select_account",
            state=state,
        )

    def fetch_token(self, code) -> Result[dict, str]:
        body = self.client.prepare_request_body(
            code=code,
            redirect_uri=self.redirect_uri,
            client_secret=self.client_secret,
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
    redirect_url = client.get_authorization_url("s")
    return HttpResponseRedirect(redirect_url)


def successfully_subscribed(request):
    return render(request, "core/successfully_subscribed.html")


def unable_to_subscribe(request):
    return render(request, "core/successfully_subscribed.html")


def google_callback(request):
    if request.method == "GET":
        code = request.GET.get("code")
        state = request.GET.get("state")
        fetch_token_result = client.fetch_token(code)

        if isinstance(fetch_token_result, Err):
            return

        token = fetch_token_result.unwrap()
        access_token = token["access_token"]
        refresh_token = token["refresh_token"]

        user = models.User(
            email="test@mail.com", doc_id="123", refresh_token=refresh_token
        )
        user.save()

        return HttpResponseRedirect(reverse("successfully_subscribed"))


SEMESTER_END_DATE = "20231220T160000Z"


def gen_google_calendar_event(event):
    return {
        "summary": f"{event['course']}",
        "location": f"{event['campus']}, {event['classroom']}",
        "description": f"Grupo: {event['group']}, Docente: {event['professor']}",
        "start": {
            "dateTime": event["starts_at"],
            "timeZone": "America/Bogota",
        },
        "end": {
            "dateTime": event["ends_at"],
            "timeZone": "America/Bogota",
        },
        "recurrence": [
            f"RRULE:FREQ=WEEKLY;UNTIL={SEMESTER_END_DATE}",
        ],
    }


def get_student_schedule_table_html(student_id):
    data = {
        "actionID": "consultardatos",
        "Fecha_ini": "2023-07-31",
        "Fecha_Fin": "2023-08-05",
        "Num_Docente": "",
        "Num_Estudiante": student_id,
    }
    r = httpx.post(
        "https://artemisa.unbosque.edu.co/serviciosacademicos/EspacioFisico/Interfas/funcionesEspaciosFisicosAsigandosReporte.php",
        data=data,
    )
    if r.status_code == 200:
        return r.text
    else:
        return None


def parse_table(table):
    table = BeautifulSoup(table, "html.parser")
    assignments = []

    for row in table.find_all("tr"):
        columns = row.find_all("td")
        campus = columns[1].text.strip()
        block = columns[2].text.strip()
        classroom = columns[3].text.strip()
        group = columns[4].text.strip()
        course = columns[6].text.strip()
        date = columns[8].text.strip()
        start_time = columns[10].text.strip()
        end_time = columns[11].text.strip()
        professor = columns[12].text.strip()
        starts_at = f"{date}T{start_time}-05:00"
        ends_at = f"{date}T{end_time}-05:00"

        assignments.append(
            {
                "campus": campus,
                "block": block,
                "classroom": classroom,
                "group": group,
                "course": course,
                "starts_at": starts_at,
                "ends_at": ends_at,
                "professor": professor,
            }
        )
    return assignments


def fetch_schedule(request):
    if request.method == "POST":
        form = FetchScheduleForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data["student_id"]
            student_schedule_table_html = get_student_schedule_table_html(student_id)
            parsed_table = parse_table(student_schedule_table_html)
            new_form = SubscribeScheduleToCalendarForm(request.POST)
            return render(
                request,
                "core/show_schedule.html",
                {"assignments": parsed_table, "form": new_form},
            )

        else:
            return render(request, "core/fetch_schedule.html", {"form": form})

    else:
        form = FetchScheduleForm()
        return render(request, "core/fetch_schedule.html", {"form": form})


def subscribe_schedule_to_calendar(request):
    if request.method == "POST":
        form = SubscribeScheduleToCalendarForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data["student_id"]
            redirect_url = client.get_authorization_url(student_id)
            return HttpResponseRedirect(redirect_url)
