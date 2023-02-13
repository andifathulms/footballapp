from django.db import models


class Competition(models.Model):
    name = models.CharField(max_length=255)
    season = models.CharField(max_length=20)
