from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

from booking.models import Booking
from trainer.models import Trainer_schedule, Service, Category
from users.models import Rating


# Create your views here.


def user_page(request):
    if request.user.groups.filter(name="Client").exists():
        bookings = Booking.objects.filter(user=request.user).all()
        return render(request, "user_profile.html", {"bookings": bookings})
    else:
        schedules = Trainer_schedule.objects.filter(trainer=request.user).all()
        trainer_services = Service.objects.filter(trainer=request.user).all()
        bookings = Booking.objects.filter(trainer=request.user).all()
        categories = Category.objects.all()
        return render(request, "trainer_profile.html",
                      {
                          "schedules": schedules,
                          "trainer_services": trainer_services,
                          "categories": categories,
                          "bookings": bookings,
                      })


def specific_user(request, user_id):
    if request.method == "GET":
        ratings = Rating.objects.filter(recipient_id=user_id).all()
        user = User.objects.get(id=user_id)
        return render(request, "ratings.html", {"ratings": ratings, "recipient_id": user_id, "user": user})


def login_page(request):
    if request.method == "Get":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/user")
        else:
            return render(request, "login.html")


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/login")
    return HttpResponse("Hello, world. You're at the polls index.")


def register_page(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        client_group = Group.objects.get(name="Client")
        user.groups.add(client_group)
        user.save()
        return redirect("/login")


def add_feedback(request, user_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            rate = int(request.POST.get("rate"))
            text = request.POST.get("text")
            rating = Rating(rate=rate, text=text, recipient_id=user_id, author_id=request.user.id)
            rating.save()
            return redirect(f"/user/{user_id}")
        return HttpResponseForbidden()