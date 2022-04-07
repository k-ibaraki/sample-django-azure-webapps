from django.db import models


# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=16)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
