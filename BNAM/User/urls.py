from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_users, name="profile"),
    path("addUser/", views.add_user),
]
