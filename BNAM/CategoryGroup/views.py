from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from .models import CategoryGroup
from Budget.models import Budget
from .serializers import CategoryGroupSerializer
from .exceptions.CategoryGroupNotFound import CategoryGroupNotFound
from Budget.exceptions.BudgetNotFound import BudgetNotFound
from Budget.exceptions.BudgetCannotBeNull import BudgetCannotBeNull

class IsCategoryGroupOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CategoryGroupCreateAPIView(CreateAPIView):
    queryset = CategoryGroup.objects.all()
    serializer_class = CategoryGroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        budget_id = self.request.data.get('budget')
        if budget_id is None:
            raise BudgetCannotBeNull()
        
        try:
            budget = Budget.objects.get(pk=budget_id)
        except Budget.DoesNotExist:
            raise BudgetNotFound(budget_id)

        if budget.user != self.request.user:
            raise BudgetNotFound(budget_id)
        serializer.validated_data['budget'] = budget
        serializer.save(user=self.request.user)

class GetCategoryGroupAPIView(RetrieveAPIView, ListAPIView):
    serializer_class = CategoryGroupSerializer
    permission_classes = [IsAuthenticated, IsCategoryGroupOwner]
    queryset = CategoryGroup.objects.all()

    def get_object(self):
        obj = get_category_group(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        category_group_id = self.kwargs.get('category_group_id')
        if category_group_id is not None:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

class UpdateCategoryGroupAPIView(UpdateAPIView):
    queryset = CategoryGroup.objects.all()
    serializer_class = CategoryGroupSerializer
    permission_classes = [IsAuthenticated, IsCategoryGroupOwner]

    def get_object(self):
        obj = get_category_group(self.kwargs, self.get_queryset())
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
    
class CategoryGroupDeleteAPIView(DestroyAPIView):
    serializer_class = CategoryGroupSerializer
    permission_classes = [IsAuthenticated, IsCategoryGroupOwner]
    queryset = CategoryGroup.objects.all()

    def get_object(self):
        obj = get_category_group(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'message': 'Category Group deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

def get_category_group(kwargs, get_queryset):
    category_group_id = kwargs.get('category_group_id')
    try:
        obj = get_queryset.get(category_group_id=category_group_id)
    except CategoryGroup.DoesNotExist:
        raise CategoryGroupNotFound(category_group_id)
    return obj