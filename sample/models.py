from django.db import models
import uuid

# Create your models here.

# DBに登録するモデル


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=16)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
