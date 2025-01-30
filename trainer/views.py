from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect

import trainer
from trainer.models import Service


# Create your views here.


def trainer_page(request, trainer_id):
    if request.user.groups.filter(name='Trainer').exists():
        if request.method == "GET":
            service_categories = trainer.models.Category.objects.all()

            my_services = trainer.models.Category.objects.all()

            return render(request, "trainer.html", {"service_categories": service_categories})
        return HttpResponse("Hello, world. You're at the polls index.")
    else:
        trainer_model = User.objects.get(pk=trainer_id)
        trainer_data = trainer.models.TrainerDescription(
            trainer=trainer_model)
        trainer_schedule = trainer.models.TrainerSchedule.objects.filter(trainer=trainer_model)

        return render(request, "account.html", context={"trainer_data": trainer_data, "trainer_schedule": trainer_schedule})


def specific_trainer(request, trainer_id):
    return HttpResponse("Hello, world. You're at the polls index.")


def trainer_service_page(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def service_page(request):
    if request.method == "GET":
        services = Service.objects.all()
        return render(request, "services.html", context={"services":services})

    else:
        if request.user.groups.filter(name='Trainer').exists():
            form_data = request.POST
            service_cat = trainer.models.Category.objects.get(pk=form_data["service_cat_id"])
            service = trainer.models.Service(
                name=form_data["name"],
                price=form_data["price"],
                duration=form_data["duration"],
                category=service_cat,
                description=form_data["description"],
            )
            service.save()
            return redirect("/trainer/")
        else:
            raise HttpResponseForbidden()


def service_booking(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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
        return HttpResponse("Hello, world. You're at the polls index.")
