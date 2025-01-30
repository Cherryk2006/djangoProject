from django.urls import path

import trainer
from . import views

urlpatterns = [
    path('', views.trainer_page, name='trainer_page'),
    path('/<trainer_id>', views.specific_trainer, name='specific_trainer'),
    path("register/trainer/", trainer.views.trainer_registration, name='trainer_registration'),
]