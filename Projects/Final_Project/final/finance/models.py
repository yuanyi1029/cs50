from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Record(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    category = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)

