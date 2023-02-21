from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist")
    pass

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=64)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=200)
    category = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.item} Listing By {self.owner}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_item")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.amount} Bid For {self.bid_item} By {self.bidder}" 

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_item")
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"'{self.comment}' Comment For {self.comment_item} By {self.commenter}" 
