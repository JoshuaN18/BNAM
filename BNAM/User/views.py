from django.shortcuts import render, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class GetUserAPIView(APIView):

    def retrieve(self, request, id):
        try:
            user = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_list(self, request):
        users = UserProfile.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, id=None):
        if id is not None:
            return self.retrieve(request, id)
        else:
            return self.get_list(request)