from django.urls import path

from . import views

urlpatterns = [
    path('<booking_id>', views.specific_booking, name='specific_booking'),
    path('<booking_id>/accept', views.accept_booking, name='accept_booking'),
    path('<booking_id>/cancel', views.cancel_booking, name='cancel_booking'),
]