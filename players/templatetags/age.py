from django import template


register = template.Library()
@register.filter
def years_age(value):
    return value.total_seconds() / 60 / 60 / 24 / 365.25