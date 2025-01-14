from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def booking_page(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def specific_booking(request, booking_id):
    return HttpResponse("Hello, world. You're at the polls index.")


def accept_page(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def cancel_page(request):
    return HttpResponse("Hello, world. You're at the polls index.")
