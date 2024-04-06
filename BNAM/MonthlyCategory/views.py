from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from .models import MonthlyCategory
from .serializers import MonthlyCategorySerializer
import logging
from .exceptions.MonthlyCategoryNotFound import MonthlyCategoryNotFound
from Category.models import Category
from Category.exceptions.CategoryNotFound import CategoryNotFound
from Category.exceptions.CategoryCannotBeNull import CategoryCannotBeNull
from datetime import datetime


class IsMonthlyCategoryOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        logger = logging.getLogger(__name__)
        logger.warning(obj.user)
        logger.warning(request.user)
        return obj.user == request.user

class MonthlyCategoryCreateAPIView(CreateAPIView):
    queryset = MonthlyCategory.objects.all()
    serializer_class = MonthlyCategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        category_id = self.request.data.get('category_id')
        if category_id is None:
            raise CategoryCannotBeNull()
        
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise CategoryNotFound(category_id)
        serializer.validated_data['category'] = category
        
        if category.user != self.request.user:
            raise CategoryNotFound(category_id)

        serializer.save(user=self.request.user)
    

class GetMonthlyCategoryAPIView(RetrieveAPIView, ListAPIView):
    serializer_class = MonthlyCategorySerializer
    permission_classes = [IsAuthenticated, IsMonthlyCategoryOwner]
    queryset = MonthlyCategory.objects.all()

    def get_object(self):
        obj = get_monthly_category(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        monthly_category_id = self.kwargs.get('monthly_category_id')
        if monthly_category_id is not None:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        # Filter queryset based on year and month
        if year and month:
            # Assuming MonthlyCategory has fields 'year' and 'month' for filtering
            self.queryset = self.queryset.filter(year=year, month=month, user=request.user)
        else:
            # If year and month are not provided, just filter by user
            self.queryset = self.queryset.filter(user=request.user)

        return super().list(request, *args, **kwargs)
    
class UpdateMonthlyCategoryAPIView(UpdateAPIView):
    queryset = MonthlyCategory.objects.all()
    serializer_class = MonthlyCategorySerializer
    permission_classes = [IsAuthenticated, IsMonthlyCategoryOwner]

    def get_object(self):
        obj = get_monthly_category(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(self.request, instance)
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MonthlyCategoryDeleteAPIView(DestroyAPIView):
    # Potentially remove it

    serializer_class = MonthlyCategorySerializer
    permission_classes = [IsAuthenticated, IsMonthlyCategoryOwner]
    queryset = MonthlyCategory.objects.all()

    def get_object(self):
        obj = get_monthly_category(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'message': 'Monthly Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
def get_monthly_category(kwargs, get_queryset):
    monthly_category_id = kwargs.get('monthly_category_id')
    try:
        obj = get_queryset.get(monthly_category_id=monthly_category_id)
    except MonthlyCategory.DoesNotExist:
        raise MonthlyCategoryNotFound(monthly_category_id)
    return obj