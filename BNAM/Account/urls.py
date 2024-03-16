from django.urls import path
from .views import AccountCreateAPIView, GetAccountAPIView, UpdateAccountAPIView, AccountDeleteAPIView

urlpatterns = [
    path("", GetAccountAPIView.as_view(), name="get_accounts"),
    path("create/", AccountCreateAPIView.as_view(), name="create_account"),
    path("<uuid:account_id>/", GetAccountAPIView.as_view(), name="get_account"),
    path("update/<uuid:account_id>/", UpdateAccountAPIView.as_view(), name="update_account"),
    path("delete/<uuid:account_id>/", AccountDeleteAPIView.as_view(), name="delete_account"),
]