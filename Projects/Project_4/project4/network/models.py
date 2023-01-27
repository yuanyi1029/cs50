from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="poster") 
    likers = models.ManyToManyField("User", blank=True, related_name="likers")
    content = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content} by {self.poster} on {self.time}"

class Profile(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="userprofile")
    followers = models.ManyToManyField("User", blank=True, related_name="follower")
    followings = models.ManyToManyField("User", blank=True, related_name="following")

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="postcomment")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="usercomment")
    content = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)
