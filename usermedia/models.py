from django.db import models
from account.models import *


# Create your models here.


class MediaPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=300, null=True, blank=True)
    media = models.TextField(max_length=500, null=True, blank=True)
    is_view = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_like = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_share = models.PositiveIntegerField(default=0, blank=True, null=True)
    # is_media = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)


class MediaView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(MediaPost, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


class MediaLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(MediaPost, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


class MediaShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(MediaPost, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
