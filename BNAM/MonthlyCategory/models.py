from django.conf import settings
from django.db import models
import uuid
from Category.models import Category

class MonthlyCategory(models.Model):
    monthly_category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monthly_category_name = models.CharField(max_length=50, default="Checking")
    month_year = models.DateField(auto_now_add=True)
    activity = models.FloatField()
    assigned = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, editable=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=True, null=False)

    def __str__(self):
        return self.monthly_category_name