from django.shortcuts import render, HttpResponse
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.exceptions import NotFound
import logging
class IsBudgetOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        logger = logging.getLogger(__name__)
        logger.warning(obj.id)
        logger.warning(request.user)
        return obj.id == request.user.id


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
        
class UpdateUserAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsBudgetOwner]

    def get_queryset(self):
        return UserProfile.objects.all()

    def get_object(self):
        user_id = self.kwargs.get('id')
        queryset = self.get_queryset()
        obj = queryset.filter(id=user_id).first()
        if obj is None:
            raise NotFound("User not found")
        self.check_object_permissions(self.request, obj)
        return obj
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserDeleteAPIView(DestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsBudgetOwner]

    def get_object(self):
        id = self.kwargs.get('id')
        try:
            obj = self.get_queryset().get(id=id)
        except UserProfile.DoesNotExist:
            raise NotFound("Budget not found")
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)