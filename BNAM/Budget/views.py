from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from .models import Budget
from .serializers import BudgetSerializer
import logging
from rest_framework.exceptions import NotFound

class IsBudgetOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        logger = logging.getLogger(__name__)
        logger.warning(obj.user)
        logger.warning(request.user)
        return obj.user == request.user

class BudgetCreateAPIView(CreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class GetBudgetAPIView(RetrieveAPIView, ListAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated, IsBudgetOwner]
    queryset = Budget.objects.all()

    def get_object(self):
        budget_id = self.kwargs.get('budget_id')
        try:
            obj = self.get_queryset().get(budget_id=budget_id)
        except Budget.DoesNotExist:
            raise NotFound("Budget not found")
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        budget_id = self.kwargs.get('budget_id')
        if budget_id is not None:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)
    
class UpdateBudgetAPIView(UpdateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated, IsBudgetOwner]

    def get_object(self):
        budget_id = self.kwargs.get('budget_id')
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.filter(budget_id=budget_id).first()
        if obj is None:
            raise NotFound("Budget not found")
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
    
class BudgetDeleteAPIView(DestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated, IsBudgetOwner]
    queryset = Budget.objects.all()

    def get_object(self):
        budget_id = self.kwargs.get('budget_id')
        try:
            obj = self.get_queryset().get(budget_id=budget_id)
        except Budget.DoesNotExist:
            raise NotFound("Budget not found")
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'message': 'Budget deleted successfully'}, status=status.HTTP_204_NO_CONTENT)