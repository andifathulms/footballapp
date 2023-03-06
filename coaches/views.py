from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse

from .forms import CoachCreationForm


def add(request: HttpRequest) -> HttpResponse:

    form = CoachCreationForm(data=request.POST or None)
    if form.is_valid():
        coach = form.save()
        messages.success(request, f"Coach successfully created. {coach} ({coach.get_current_teams})")
        return redirect(reverse("coaches:add"))

    context_data = {
        "title": "Add Coach",
        "current_page": "coaches",
        "form": form
    }
    return render(request, "coaches/add.html", context_data)