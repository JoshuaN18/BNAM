from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.getUsers, name="profile"),
    path("addUser/", views.addUser),
]
