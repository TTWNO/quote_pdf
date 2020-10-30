import json
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CalgaryAddress(models.Model):
    address = models.CharField(max_length=32)
    house_alpha = models.CharField(max_length=1)
    street_quad = models.CharField(max_length=2)
    street_name = models.CharField(max_length=16)
    street_type = models.CharField(max_length=2)

    def toDict(self):
        return {
            'address': self.address
        }

class QuoteUser(User):
    pass