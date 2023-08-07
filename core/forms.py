from django import forms


class FetchScheduleForm(forms.Form):
    student_id = forms.CharField(label="N° Documento Estudiante", required=True)


class SubscribeScheduleToCalendarForm(forms.Form):
    student_id = forms.CharField(
        label="N° Documento Estudiante", required=True, widget=forms.HiddenInput()
    )
