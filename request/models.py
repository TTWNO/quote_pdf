from django.db import models
from core.models import QuoteUser
from download.models import Address

# Create your models here.
class QuoteRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='quote_requests')
    user = models.ForeignKey(QuoteUser, on_delete=models.CASCADE, related_name='quote_requests')