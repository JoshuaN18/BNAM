from django.urls import path
from .views import CategoryGroupCreateAPIView, GetCategoryGroupAPIView, UpdateCategoryGroupAPIView, CategoryGroupDeleteAPIView

urlpatterns = [
    path("", GetCategoryGroupAPIView.as_view(), name="get_category_groups"),
    path("create/", CategoryGroupCreateAPIView.as_view(), name="create_category_group"),
    path("<uuid:category_group_id>/", GetCategoryGroupAPIView.as_view(), name="get_category_group"),
    path("update/<uuid:category_group_id>/", UpdateCategoryGroupAPIView.as_view(), name="update_category_group"),
    path("delete/<uuid:category_group_id>/", CategoryGroupDeleteAPIView.as_view(), name="delete_category_group"),
]