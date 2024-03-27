from django.urls import path
from .views import SignupAPIView

from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
app_name = 'authentication'
urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]