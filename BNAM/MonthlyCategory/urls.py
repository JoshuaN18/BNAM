from django.urls import path
from .views import MonthlyCategoryCreateAPIView, GetMonthlyCategoryAPIView, UpdateMonthlyCategoryAPIView

urlpatterns = [
    path("", GetMonthlyCategoryAPIView.as_view(), name="get_monthly_categories"),
    path("create/", MonthlyCategoryCreateAPIView.as_view(), name="create_monthly_category"),
    path("<uuid:monthly_category_id>/", GetMonthlyCategoryAPIView.as_view(), name="get_monthly_category"),
    path("update/<uuid:monthly_category_id>/", UpdateMonthlyCategoryAPIView.as_view(), name="update_monthly_category"),
]