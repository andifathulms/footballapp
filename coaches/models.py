from django.db import models
from regions.models import Country


class Coach(models.Model):
    name = models.CharField(max_length=255)
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
