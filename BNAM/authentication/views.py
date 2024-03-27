from User.models import UserProfile
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . serializers import SignupSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class SignupAPIView(APIView):

    permission_classes = []
    def post(self, request):
        
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)
        
        if password == confirm_password: 
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            response = status.HTTP_202_ACCEPTED

        else:
            data = ''
            raise ValidationError({'password_mismatch': 'Password fields didn not match.'})     
        return Response(data, status=response)