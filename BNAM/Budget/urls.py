from django.urls import path
from .views import BudgetCreateAPIView, GetBugetAPIView

urlpatterns = [
    path("", GetBugetAPIView.as_view(), name="get_budgets"),
    path("create/", BudgetCreateAPIView.as_view(), name="create_budget"),
    path("<uuid:budget_id>/", GetBugetAPIView.as_view(), name="get_budget"),
]
