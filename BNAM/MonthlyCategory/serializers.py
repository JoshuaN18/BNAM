from rest_framework import serializers
from .models import MonthlyCategory
from Category.models import Category  # Import Category model
from Category.serializers import CategorySerializer

class MonthlyCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(write_only=True)  # Add this field for category UUID input

    class Meta:
        model = MonthlyCategory
        fields = ['monthly_category_id', 'monthly_category_name', 'month', 'year', 'activity', 'assigned', 'category_id', 'user']
        read_only_fields = ['monthly_category_id', 'user']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category).data
        return rep

    def create(self, validated_data):
        # Extract and remove category_id from validated_data
        category_id = validated_data.pop('category_id')

        # Get or create category using category_id
        category = Category.objects.get(category_id=category_id)

        # Assign category to validated_data
        validated_data['category'] = category

        # Call super() to create MonthlyCategory instance
        monthly_category = super().create(validated_data)

        return monthly_category
