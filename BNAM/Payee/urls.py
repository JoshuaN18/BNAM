from django.urls import path
from .views import PayeeCreateAPIView, GetPayeeAPIView, UpdatePayeeAPIView, PayeeDeleteAPIView

urlpatterns = [
    path("", GetPayeeAPIView.as_view(), name="get_payees"),
    path("create/", PayeeCreateAPIView.as_view(), name="create_payee"),
    path("<uuid:payee_id>/", GetPayeeAPIView.as_view(), name="get_payee"),
    path("update/<uuid:payee_id>/", UpdatePayeeAPIView.as_view(), name="update_payee"),
    path("delete/<uuid:payee_id>/", PayeeDeleteAPIView.as_view(), name="delete_payee"),
]
