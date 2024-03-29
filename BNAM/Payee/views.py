from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from .models import Payee
from .serializers import PayeeSerializer
from .exceptions.PayeeNotFound import PayeeNotFound

class IsPayeeOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class PayeeCreateAPIView(CreateAPIView):
    queryset = Payee.objects.all()
    serializer_class = PayeeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class GetPayeeAPIView(RetrieveAPIView, ListAPIView):
    serializer_class = PayeeSerializer
    permission_classes = [IsAuthenticated, IsPayeeOwner]
    queryset = Payee.objects.all()

    def get_object(self):
        obj = get_payee(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        payee_id = self.kwargs.get('payee_id')
        if payee_id is not None:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)
    
class UpdatePayeeAPIView(UpdateAPIView):
    queryset = Payee.objects.all()
    serializer_class = PayeeSerializer
    permission_classes = [IsAuthenticated, IsPayeeOwner]

    def get_object(self):
        obj = get_payee(self.kwargs, self.get_queryset())
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
    
class PayeeDeleteAPIView(DestroyAPIView):
    serializer_class = PayeeSerializer
    permission_classes = [IsAuthenticated, IsPayeeOwner]
    queryset = Payee.objects.all()

    def get_object(self):
        obj = get_payee(self.kwargs, self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({'message': 'Payee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
def get_payee(kwargs, get_queryset):
    payee_id = kwargs.get('payee_id')
    try:
        obj = get_queryset.get(payee_id=payee_id)
    except Payee.DoesNotExist:
        raise PayeeNotFound(payee_id)
    return obj