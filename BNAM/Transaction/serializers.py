from rest_framework import serializers
from .models import Transaction
from Category.models import Category
from Payee.models import Payee
from Category.serializers import CategorySerializer
from Payee.serializers import PayeeSerializer

class TransactionSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(write_only=True)
    payee_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'date', 'cleared', 'lock', 'outflow', 'inflow', 'category_id', 'payee_id', 'user']
        read_only_fields = ['transaction_id', 'user']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category).data
        rep['payee'] = PayeeSerializer(instance.payee).data
        return rep

    def create(self, validated_data):
        # Extract and remove category_id and payee_id from validated_data
        category_id = validated_data.pop('category_id')
        payee_id = validated_data.pop('payee_id')

        # Get or create category using category_id
        category = Category.objects.get(pk=category_id)

        # Get or create payee using payee_id
        payee = Payee.objects.get(pk=payee_id)

        # Assign category and payee to validated_data
        validated_data['category'] = category
        validated_data['payee'] = payee

        # Call super() to create Transaction instance
        transaction = super().create(validated_data)

        return transaction
