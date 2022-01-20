from django.db import models
# Create your models here.
from django.db.models import Count
from django.db.models.signals import pre_save
from django.dispatch import receiver

from account.models import *


class PostUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255, blank=True, null=True, default="title")
    message = models.TextField(default="messages", blank=True, null=True)
    post = models.URLField(blank=True, null=True)
    is_view = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_like = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_share = models.PositiveIntegerField(default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)


class PostReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Reaction")
    post = models.ForeignKey(PostUpload, on_delete=models.CASCADE, related_name="Reaction")
    # is_view = models.IntegerField(default=0, blank=True, null=True)
    # is_like = models.IntegerField(default=0, blank=True, null=True)
    # is_share = models.IntegerField(default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)


class MediaPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=300, null=True, blank=True)
    media = models.TextField(max_length=500, null=True, blank=True)
    is_view = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_like = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_share = models.PositiveIntegerField(default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

class MediaReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(MediaPost, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
