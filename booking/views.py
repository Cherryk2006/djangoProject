from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from booking.models import Booking
from trainer.utils import ACCEPT_STATUS


# Create your views here.

def specific_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.user == booking.user or request.user == booking.trainer:
        return render(request, "booking.html",
                      {
                          "booking": booking,
                          "is_user": request.user.groups.filter(name="Client").exists()
                      })
    else:
        return HttpResponseForbidden()


def cancel_booking(request, booking_id):
    if request.method == "POST":
        booking = Booking.objects.get(id=booking_id)
        if request.user == booking.user or request.user == booking.trainer:
            booking.delete()
            return redirect("/user")
        else:
            return HttpResponseForbidden()


def accept_booking(request, booking_id):
    if request.method == "POST":
        booking = Booking.objects.get(id=booking_id)
        if request.user == booking.trainer:
            booking.status = ACCEPT_STATUS
            booking.save()
            return redirect(f"/booking/{booking.id}")
        else:
            return HttpResponseForbidden()