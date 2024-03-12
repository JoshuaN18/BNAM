from django.urls import path
from .views import GetUserAPIView
from . import views

urlpatterns = [
    path("", GetUserAPIView.as_view(), name="list_users"),
    path("<uuid:id>/", GetUserAPIView.as_view(), name="get_user"),
]
