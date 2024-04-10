from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from .models import Transaction
from .serializers import TransactionSerializer
import logging
from .exceptions.TransactionNotFound import TransactionNotFound
from Payee.models import Payee
from Payee.exceptions.PayeeNotFound import PayeeNotFound
from Category.models import Category
from Category.exceptions.CategoryNotFound import CategoryNotFound
from Category.exceptions.CategoryCannotBeNull import CategoryCannotBeNull


class IsTransactionOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        logger = logging.getLogger(__name__)
        logger.warning(obj.user)
        logger.warning(request.user)
        return obj.user == request.user

class TransactionCreateAPIView(CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        category_id = self.request.data.get('category_id')
        payee_id = self.request.data.get('payee_id')
        if category_id is None:
            raise CategoryCannotBeNull()
        
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise CategoryNotFound(category_id)
        
        try:
            payee = Payee.objects.get(pk=payee_id)
        except Payee.DoesNotExist:
            raise PayeeNotFound(payee_id)
        
        serializer.validated_data['category'] = category
        serializer.validated_data['payee'] = payee
        
        if category.user != self.request.user:
            raise CategoryNotFound(category_id)
        if payee.user != self.request.user:
            raise PayeeNotFound(payee_id)

        serializer.save(user=self.request.user)
    

class GetTransactionAPIView(RetrieveAPIView, ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsTransactionOwner]
    queryset = Transaction.objects.all()

    def get_object(self):
        obj = get_transaction(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        transaction_id = self.kwargs.get('transaction_id')
        if transaction_id is not None:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)
    
class UpdateTransactionAPIView(UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsTransactionOwner]

    def get_object(self):
        obj = get_transaction(self.kwargs, self.get_queryset())
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
    
class TransactionDeleteAPIView(DestroyAPIView):

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsTransactionOwner]
    queryset = Transaction.objects.all()

    def get_object(self):
        obj = get_transaction(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'message': 'Transaction deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
def get_transaction(kwargs, get_queryset):
    transaction_id = kwargs.get('transaction_id')
    try:
        obj = get_queryset.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        raise TransactionNotFound(transaction_id)
    return obj