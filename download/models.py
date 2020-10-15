from django.db import models
from core.models import CalgaryAddress
from .validators import RestrictedFileField

# Create your models here.
class PDF(models.Model):
    path = models.CharField(max_length=64)
    code = models.CharField(max_length=8)
    address_string = models.CharField(max_length=32)
    address = models.ForeignKey(CalgaryAddress, related_name='pdfs', on_delete=models.CASCADE)
    upload_file = RestrictedFileField(max_upload_size=1024*1024*1024*50, content_types=['pdf', 'application/pdf'], upload_to='uploads/%Y/%m/%d/')
