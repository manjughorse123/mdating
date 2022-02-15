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
    uploadvedio = models.TextField( blank=True, null=True)
    is_view = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_like = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_share = models.PositiveIntegerField(default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostUpload, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostUpload, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


class PostShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostUpload, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
