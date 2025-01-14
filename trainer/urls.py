from django.urls import path

from . import views

urlpatterns = [
    path('', views.trainer_page, name='trainer_page'),
    path('/<trainer_id>', views.specific_trainer, name='specific_trainer'),
]