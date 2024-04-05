from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from .models import Category
from Budget.models import Budget
from CategoryGroup.models import CategoryGroup
from .serializers import CategorySerializer
from CategoryGroup.exceptions.CategoryGroupNotFound import CategoryGroupNotFound
from CategoryGroup.exceptions.CategoryGroupDoesNotBelongToBudget import CategoryGroupDoesNotBelongToBudget
from Budget.exceptions.BudgetNotFound import BudgetNotFound
from Budget.exceptions.BudgetCannotBeNull import BudgetCannotBeNull
from .exceptions.CategoryNotFound import CategoryNotFound


class IsCategoryOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        budget_id = self.request.data.get('budget')
        if budget_id is None:
            raise BudgetCannotBeNull()
        try:
            budget = Budget.objects.get(pk=budget_id)
        except Budget.DoesNotExist:
            raise BudgetNotFound(budget_id)
        
        serializer.validated_data['budget'] = budget
        category_group_id = self.request.data.get('category_group')
        if category_group_id != None:
            try:
                category_group = CategoryGroup.objects.get(pk=category_group_id)
            except CategoryGroup.DoesNotExist:
                raise CategoryGroupNotFound(category_group_id)
            
            serializer.validated_data['category_group'] = category_group
            if category_group.budget != budget:
                raise CategoryGroupDoesNotBelongToBudget(category_group_id, budget_id)
            serializer.validated_data['category_group'] = category_group

        if budget.user != self.request.user:
            raise BudgetNotFound(budget_id)
        
        
        serializer.save(user=self.request.user)

class GetCategoryAPIView(RetrieveAPIView, ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsCategoryOwner]
    queryset = Category.objects.all()

    def get_object(self):
        obj = get_category(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        category_id = self.kwargs.get('category_id')
        if category_id is not None:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

class UpdateCategoryAPIView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsCategoryOwner]

    def get_object(self):
        obj = get_category(self.kwargs, self.get_queryset())
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
    
class CategoryDeleteAPIView(DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsCategoryOwner]
    queryset = Category.objects.all()

    def get_object(self):
        obj = get_category(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
def get_category(kwargs, get_queryset):
    category_id = kwargs.get('category_id')
    try:
        obj = get_queryset.get(category_id=category_id)
    except Category.DoesNotExist:
        raise CategoryNotFound(category_id)
    return obj