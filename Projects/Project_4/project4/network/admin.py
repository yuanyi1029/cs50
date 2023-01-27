from django.contrib import admin
from .models import User, Post, Profile, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("likers",)

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ("followers", "followings",)

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment)
