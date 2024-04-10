from django.urls import path
from .views import TransactionCreateAPIView, GetTransactionAPIView, UpdateTransactionAPIView, TransactionDeleteAPIView

urlpatterns = [
    path("", GetTransactionAPIView.as_view(), name="get_transactions"),
    path("create/", TransactionCreateAPIView.as_view(), name="create_transaction"),
    path("<uuid:transaction_id>/", GetTransactionAPIView.as_view(), name="get_transaction"),
    path("update/<uuid:transaction_id>/", UpdateTransactionAPIView.as_view(), name="update_transaction"),
    path("delete/<uuid:transaction_id>/", TransactionDeleteAPIView.as_view(), name="delete_transaction"),
]