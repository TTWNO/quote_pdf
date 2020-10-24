from django.db import models
from core.models import CalgaryAddress
from .validators import RestrictedFileField

# Create your models here.
class Address(models.Model):
    address = models.CharField(max_length=128)
    # TODO: add validation columns in relation to city
    city = models.CharField(max_length=32)

class PDF(models.Model):
    path = models.CharField(max_length=64)
    code = models.CharField(max_length=8)
    upload_file = RestrictedFileField(max_upload_size=1024*1024*50, content_types=['pdf', 'application/pdf'], upload_to='uploads/%Y/%m/%d/')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='uploads')
    upload_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
