from django.urls import path

import trainer
from . import views

urlpatterns = [
    path('', views.trainer_page, name='trainer_page'),
    path('<trainer_id>', views.specific_trainer, name='specific_trainer'),
    path('<trainer_id>/<service_id>', views.specific_service, name='specific_service'),
    path('<trainer_id>/<service_id>/booking', views.book_service, name='book_service'),
    path('services/', views.add_service, name='add_service'),
    path("register/trainer/", trainer.views.trainer_registration, name='trainer_registration'),
    path("schedule/", trainer.views.add_schedule, name='add_schedule'),
]