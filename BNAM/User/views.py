from django.shortcuts import render, HttpResponse
from rest_framework import response, status
from rest_framework.decorators import api_view, permission_classes
from .models import UserProfile
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = UserProfile.objects.all()
    serializer = UserSerializer(users, many=True)

    return response.Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return response.Response(serializer.data)