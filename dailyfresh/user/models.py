from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=11,default='')
    address = models.CharField(max_length=128,default='')
