from django.urls import path
from .views import BudgetCreateAPIView, GetBugetAPIView, UpdateBudgetAPIView, BudgetDeleteAPIView

urlpatterns = [
    path("", GetBugetAPIView.as_view(), name="get_budgets"),
    path("create/", BudgetCreateAPIView.as_view(), name="create_budget"),
    path("<uuid:budget_id>/", GetBugetAPIView.as_view(), name="get_budget"),
    path("update/<uuid:budget_id>/", UpdateBudgetAPIView.as_view(), name="update_budget"),
    path("delete/<uuid:budget_id>/", BudgetDeleteAPIView.as_view(), name="delete_budget")
]
