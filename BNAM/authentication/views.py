from User.models import UserProfile
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . serializers import SignupSerializer
import logging
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