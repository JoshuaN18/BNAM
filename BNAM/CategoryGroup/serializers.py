from rest_framework import serializers
from .models import CategoryGroup

class CategoryGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryGroup
        fields = ['category_group_id', 'category_group_name', 'budget', 'user']
        read_only_fields = ['user', 'category_group_id', 'budget']