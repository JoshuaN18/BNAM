from django.conf import settings
from django.db import models
import uuid
from Category.models import Category
from Payee.models import Payee
import datetime


class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=datetime.date.today)
    cleared = models.BooleanField()
    lock = models.BooleanField()
    outflow = models.FloatField()
    inflow = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, editable=True, null=True)
    payee = models.ForeignKey(Payee, on_delete=models.SET_NULL, editable=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=True, null=False)
