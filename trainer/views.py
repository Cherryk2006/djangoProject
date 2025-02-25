import datetime

from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect

from booking.models import Booking
from trainer.models import Service, Category, Trainer_description, Trainer_schedule
from trainer.utils import booking_time_discovery, PROCESSING_STATUS


# Create your views here.


def trainer_page(request):
    category_id = int(request.GET.get('category', "-1"))

    if category_id == -1:
        trainers = Trainer_description.objects.all()
    else:
        trainers = Trainer_description.objects.filter(trainer__service__category_id=category_id)

    categories = Category.objects.all()
    return render(request, "trainers.html",
                  {
                      "trainers": trainers,
                      "categories": categories,
                      "category_id": category_id
                  })


def specific_trainer(request, trainer_id):
    trainer = Trainer_description.objects.filter(trainer_id=trainer_id).first()
    services = Service.objects.filter(trainer_id=trainer_id)
    return render(request, "trainer.html",
                  {
                      "trainer": trainer,
                      "services": services,
                      "is_user": request.user.groups.filter(name="Client").exists()
                  })


def trainer_registration(request):
    if request.method == "GET":
        return render(request, "trainer_signup.html")
    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        trainer_group = Group.objects.get(name="Trainer")
        user.groups.add(trainer_group)
        user.save()

        trainer_description = Trainer_description(text=request.POST.get("description"), trainer=user)
        trainer_description.save()

        return redirect("/login")

def add_service(request):
    if request.method == "POST":
        if request.user.groups.filter(name='Trainer').exists():
            category = Category.objects.filter(name=request.POST.get("category")).first()
            price = float(request.POST.get("price"))
            level = int(request.POST.get("level"))
            duration = int(request.POST.get("duration"))

            service = Service(category=category, price=price, level=level, duration=duration, trainer=request.user)
            service.save()
            return redirect("/user")
        else:
            return HttpResponseForbidden()


def specific_service(request, trainer_id, service_id):
    service = Service.objects.get(id=service_id)
    schedules = Trainer_schedule.objects.filter(trainer_id=trainer_id).all()
    available_slots = []

    for schedule in schedules:
        available_slot = [_.strftime("%H:%M") for _ in booking_time_discovery(
                    schedule.datetime_start, schedule.datetime_end,
                    [[_.datetime_start, _.datetime_end] for _ in Booking.objects.filter(trainer_id=trainer_id).all()],
                    service.duration
                )]
        available_slots.append(
            {
                "date": schedule.datetime_start.strftime("%Y-%m-%d"),
                "slots": available_slot,
                "is_present": len(available_slot) > 0
            }
        )

    return render(request, "service.html",
                  {
                      "service": service,
                      "is_user": request.user.groups.filter(name="Client").exists(),
                      "available_slots": available_slots
                  })


def add_schedule(request):
    if request.method == "POST":
        if request.user.groups.filter(name='Trainer').exists():
            day = request.POST.get("day")
            start_at = request.POST.get("start_at")
            end_at = request.POST.get("end_at")

            start_at = datetime.datetime.combine(datetime.date.fromisoformat(day),
                                                 datetime.time.fromisoformat(start_at))
            end_at = datetime.datetime.combine(datetime.date.fromisoformat(day), datetime.time.fromisoformat(end_at))

            if start_at > end_at or end_at < datetime.datetime.now():
                return HttpResponseBadRequest()

            if Trainer_schedule.objects.filter(
                    datetime_start__day=start_at.day,
                    datetime_start__month=start_at.month,
                    datetime_start__year=start_at.year,
            ).exists():
                trainer_schedule = Trainer_schedule.objects.filter(
                    datetime_start__day=start_at.day,
                    datetime_start__month=start_at.month,
                    datetime_start__year=start_at.year,
                ).first()
                trainer_schedule.datetime_start = start_at
                trainer_schedule.datetime_end = end_at
            else:
                trainer_schedule = Trainer_schedule(
                    trainer=request.user, datetime_start=start_at, datetime_end=end_at
                )

            trainer_schedule.save()

            return redirect("/user")
        else:
            return HttpResponseForbidden()


def book_service(request, trainer_id, service_id):
    if request.method == "POST":
        if request.user.groups.filter(name='Client').exists():
            service = Service.objects.get(id=service_id)
            trainer = User.objects.get(id=trainer_id)

            date_param = request.POST.get("date")
            time_param = request.POST.get("time")

            start_at = datetime.datetime.combine(datetime.date.fromisoformat(date_param), datetime.time.fromisoformat(time_param))
            end_at = start_at + datetime.timedelta(minutes=service.duration)

            booking = Booking(
                user=request.user,
                trainer=trainer,
                service=service,
                datetime_start=start_at,
                datetime_end=end_at,
                status=PROCESSING_STATUS
            )

            booking.save()

            return redirect("/user")
        else:
            return HttpResponseForbidden()