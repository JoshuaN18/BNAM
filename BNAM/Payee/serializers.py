from rest_framework import serializers
from .models import Payee

class PayeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payee
        fields = ['payee_id', 'payee_name', 'user']
        read_only_fields = ['user']