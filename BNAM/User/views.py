from django.shortcuts import render, HttpResponse
from rest_framework import response, status
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer

# Create your views here.
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return response.Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return response.Response(serializer.data)