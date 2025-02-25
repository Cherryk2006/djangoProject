from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_page, name='user_page'),
    path('<user_id>', views.specific_user, name='specific_user'),
    path('<user_id>/add-feedback', views.add_feedback, name='add_feedback'),

]