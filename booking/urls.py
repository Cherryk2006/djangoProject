from django.urls import path

from . import views

urlpatterns = [
    path('', views.booking_page, name='booking_page'),
    path('/<booking_id>', views.specific_booking, name='specific_booking'),
]