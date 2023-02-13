from django.db import models
from model_utils import Choices


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey('Province', related_name='cities', on_delete=models.CASCADE)
    country = models.ForeignKey('Country', related_name='cities', on_delete=models.CASCADE)

    TYPE = Choices(
        (1, 'kabupaten', 'Kabupaten'),
        (2, 'kota', 'Kota'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPE, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
