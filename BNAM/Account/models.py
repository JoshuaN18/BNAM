from django.db import models
import uuid
from django.conf import settings
from Budget.models import Budget

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('Savings', 'Savings'),
        ('Checking', 'Checking'),
        ('Investment', 'Investment'),
        ('Credit', 'Credit'),
    ]

    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_name = models.CharField(max_length=50, blank=True, default="Budget")
    account_type = models.CharField(max_length=50, default="Checking", choices=ACCOUNT_TYPE_CHOICES)
    balance = models.FloatField(default=0)
    cleared_balance = models.FloatField(default=0)
    uncleared_balance = models.FloatField(default=0)
    working_balance = models.FloatField(default=0)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, editable=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=True)

    def __str__(self):
        return self.account_name