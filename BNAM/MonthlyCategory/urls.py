from django.urls import path
from .views import MonthlyCategoryCreateAPIView, GetMonthlyCategoryAPIView, UpdateMonthlyCategoryAPIView

urlpatterns = [
    path("", GetMonthlyCategoryAPIView.as_view(), name="get_category_groups"),
    path("create/", MonthlyCategoryCreateAPIView.as_view(), name="create_category_group"),
    path("<uuid:category_group_id>/", GetMonthlyCategoryAPIView.as_view(), name="get_category_group"),
    path("update/<uuid:category_group_id>/", UpdateMonthlyCategoryAPIView.as_view(), name="update_category_group"),
]