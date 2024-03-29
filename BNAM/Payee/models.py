from django.conf import settings
from django.db import models
import uuid

class Payee(models.Model):
    payee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payee_name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=True)

    def __str__(self):
        return self.payee_name