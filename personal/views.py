from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    context_data = {}
    return render(request, 'main.html', context_data)
