from django.db import models
from regions.models import City


class Stadium(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, related_name='stadiums', on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)
    year_of_opened = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
