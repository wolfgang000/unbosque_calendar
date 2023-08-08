from django.db import models


class User(models.Model):
    email = models.EmailField()
    doc_id = models.CharField(max_length=30)
    refresh_token = models.CharField()
    calendar_id = models.CharField()
