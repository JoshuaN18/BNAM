from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name', 'target_type', 'target_amount', 'order', 'budget', 'category_group', 'user']
        read_only_fields = ['user', 'category_id', 'budget']