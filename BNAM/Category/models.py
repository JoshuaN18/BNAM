from django.db import models
from Budget.models import Budget
from CategoryGroup.models import CategoryGroup
from django.conf import settings
import uuid

class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=50)
    target_type = models.CharField(max_length=50)
    target_amount = models.FloatField()
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, editable=True)
    order = models.IntegerField()
    category_group = models.ForeignKey(CategoryGroup, on_delete=models.SET_NULL, null=True, blank=True, editable=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=True)


    def __str__(self):
        return self.category_name