from django.contrib import admin

from .models import City, Province, Country

class CityAdmin(admin.ModelAdmin):
    model = City
    ordering = ('type', 'name')

admin.site.register(City, CityAdmin)
admin.site.register(Province)
admin.site.register(Country)
