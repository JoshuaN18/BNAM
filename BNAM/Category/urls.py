from django.urls import path
from .views import CategoryCreateAPIView, GetCategoryAPIView, UpdateCategoryAPIView, CategoryDeleteAPIView

urlpatterns = [
    path("", GetCategoryAPIView.as_view(), name="get_categories"),
    path("create/", CategoryCreateAPIView.as_view(), name="create_category"),
    path("<uuid:category_id>/", GetCategoryAPIView.as_view(), name="get_category"),
    path("update/<uuid:category_id>/", UpdateCategoryAPIView.as_view(), name="update_category"),
    path("delete/<uuid:category_id>/", CategoryDeleteAPIView.as_view(), name="delete_category"),
]