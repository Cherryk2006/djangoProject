"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


import booking
import users.views
import booking.views
import trainer.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('login/', users.views.login_page, name='users_login'),
    path('logout/', users.views.logout_page, name='users_logout'),
    path('register/', users.views.register_page, name='users_register'),
    path('booking/', include('booking.urls')),
    path('accept_booking/', booking.views.accept_page, name='accept_booking'),
    path('cancel_booking/', booking.views.cancel_page, name='cancel_booking'),
    path('trainer/', include('trainer.urls')),
    path('service/', trainer.views.service_page, name='trainer_service'),
    path('book_service/', trainer.views.service_booking, name='book_service'),
]
