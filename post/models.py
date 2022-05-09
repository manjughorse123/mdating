from django.db import models
# Create your models here.
from django.db.models import Count
from django.db.models.signals import pre_save

from account.models import *

MAYBECHOICE = (
    (0, 'all'),
    (1, 'friend'),
    (2, 'onlyme'),
)


class PostUpload(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255, blank=True,
                             null=True, default="title")
    message = models.TextField(default="messages", blank=True, null=True)
    post = models.TextField(blank=True, null=True)
    uploadvideo = models.TextField(blank=True, null=True)
    is_view_count = models.PositiveIntegerField(
        default=0, blank=True, null=True)
    is_like_count = models.PositiveIntegerField(
        default=0, blank=True, null=True)
    is_share_count = models.PositiveIntegerField(
        default=0, blank=True, null=True)
    post_report = models.BooleanField(
        default=False, blank=True, null=True)
    is_private = models.PositiveIntegerField(
        default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    show_public_post = models.IntegerField(
        choices=MAYBECHOICE, default=0)
    show_private_post = models.IntegerField(
        choices=MAYBECHOICE, default=0)

    def __str__(self):
        return str(self.id)+','+str(self.post)


class PostView(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="postview")
    post = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="postsview")
    is_view = models.PositiveIntegerField(default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.post


class PostLike(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="postlike")
    post = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="postlike")
    is_like = models.BooleanField(blank=True, null=True, default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.post


class PostShare(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="postshare")
    post = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="postshare")
    is_share = models.PositiveIntegerField(default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.post


class PostReport(models.Model):

    post = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="postreplike")
    report_text = models.CharField(max_length=255, blank=True, null=True,)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.post


class PostImage(models.Model):

    post = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="postimages")
    post_image = models.CharField(max_length=255, blank=True, null=True,)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.post
