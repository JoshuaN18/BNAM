from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from .models import Account
from Budget.models import Budget
from .serializers import AccountSerializer
from rest_framework.exceptions import NotFound, ValidationError

class IsAccountOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class AccountCreateAPIView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        budget_id = self.request.data.get('budget')
        if budget_id is None:
            raise ValidationError({'message': 'budget cannot be null'})
        try:
            budget = Budget.objects.get(pk=budget_id)
        except Budget.DoesNotExist:
            raise ValidationError({'message': f'Budget with ID {budget_id} does not exist'})

        if budget.user != self.request.user:
            raise ValidationError({'message': f'Budget with ID {budget_id} does not exist'})
        serializer.validated_data['budget'] = budget
        serializer.save(user=self.request.user)

class GetAccountAPIView(RetrieveAPIView, ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]
    queryset = Account.objects.all()

    def get_object(self):
        account_id = self.kwargs.get('account_id')
        try:
            obj = self.get_queryset().get(account_id=account_id)
        except Account.DoesNotExist:
            raise NotFound("Account not found")
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        account_id = self.kwargs.get('account_id')
        if account_id is not None:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)

class UpdateAccountAPIView(UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def get_object(self):
        account_id = self.kwargs.get('account_id')
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.filter(account_id=account_id).first()
        if obj is None:
            raise NotFound("Account not found")
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
    
class AccountDeleteAPIView(DestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]
    queryset = Account.objects.all()

    def get_object(self):
        account_id = self.kwargs.get('account_id')
        try:
            obj = self.get_queryset().get(account_id=account_id)
        except Account.DoesNotExist:
            raise NotFound("Account not found")
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)