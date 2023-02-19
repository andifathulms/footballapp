from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def add(request: HttpRequest) -> HttpResponse:

    form = PlayerCreationForm(data=request.POST or None, customer=customer)
    if form.is_valid():
        booking = form.save(created_by=user)
        messages.success(request, "Booking successfully created")
        return redirect(reverse("customers:bookings:details", args=[booking.id]))

    context_data = {
        "title": "Add Player",
        "current_page": "players",
        "form": form
    }
    return render(request, "players/add.html", context_data)
