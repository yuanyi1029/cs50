from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Record(models.Model):
    CATEGORY_CHOICES = [
        (1, "Food & Drinks"),
        (2, "Shopping"),
        (3, "Housing"),
        (4, "Transportation"),
        (5, "Vehicle"),
        (6, "Life & Entertainment"),
        (7, "Communication, Technology"),
        (8, "Financial Expenses"),
        (9, "Investments"),
        (10, "Income"),
        (11, "Others")
    ]

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    category = models.PositiveIntegerField(choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)

