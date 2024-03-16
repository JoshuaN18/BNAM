from django.db import models
import uuid
from django.conf import settings
from Budget.models import Budget

class CategoryGroup(models.Model):
    category_group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_group_name = models.CharField(max_length=50, default="Checking", null=False)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.category_group_name