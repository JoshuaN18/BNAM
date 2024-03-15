from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_id', 'account_name', 'account_type', 'balance', 'cleared_balance', 'uncleared_balance', 'working_balance', 'budget', 'user']
        read_only_fields = ['user', 'account_id', 'budget']