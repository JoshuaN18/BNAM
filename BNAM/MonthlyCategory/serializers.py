from rest_framework import serializers
from .models import MonthlyCategory
from Category.serializers import CategorySerializer

class MonthlyCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = MonthlyCategory
        fields = ['monthly_category_id', 'monthly_category_name', 'month_year', 'activity', 'assigned', 'category','user']
        read_only_fields = ['monthly_category_id', 'user', 'category']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category).data
        return rep

    