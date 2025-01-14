from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def trainer_page(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def specific_trainer(request, trainer_id):
    return HttpResponse("Hello, world. You're at the polls index.")


def service_page(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def service_booking(request):
    return HttpResponse("Hello, world. You're at the polls index.")
