from django.urls import path
from .views import GetUserAPIView, UpdateUserAPIView, UserDeleteAPIView
from . import views

urlpatterns = [
    path("", GetUserAPIView.as_view(), name="list_users"),
    path("<uuid:id>/", GetUserAPIView.as_view(), name="get_user"),
    path("update/<uuid:id>/", UpdateUserAPIView.as_view(), name="update_user"),
    path("delete/<uuid:id>/", UserDeleteAPIView.as_view(), name="delete_user")
]
