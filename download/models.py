from django.db import models
from core.models import CalgaryAddress, QuoteUser
from .validators import RestrictedFileField

# Create your models here.
class Address(models.Model):
    address = models.CharField(max_length=128)
    # TODO: add validation columns in relation to city
    city = models.CharField(max_length=32)
    def toDict(self):
        return {
            'address': self.address,
            'id': self.id
        }

class PDF(models.Model):
    path = models.CharField(max_length=64)
    code = models.CharField(max_length=8)
    upload_file = RestrictedFileField(max_upload_size=1024*1024*50, content_types=['pdf', 'application/pdf'], upload_to='uploads/%Y/%m/%d/')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='uploads')
    upload_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    valid = models.BooleanField()

class EmailSent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    user = models.ForeignKey(QuoteUser, on_delete=models.CASCADE)
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=256)

class DownloadAttempt(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    user = models.ForeignKey(QuoteUser, on_delete=models.CASCADE, related_name='attempts')
    email_sent = models.BooleanField(default=False)
    code_correct = models.BooleanField(default=False)
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE, related_name='attempts')
    ip = models.GenericIPAddressField()
    geolocation = models.CharField(max_length=64)