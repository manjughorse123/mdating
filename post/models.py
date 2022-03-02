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
    post = models.TextField( blank=True, null=True)
    uploadvideo = models.TextField( blank=True, null=True)
    is_view_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_like_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_share_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postview")
    post = models.ForeignKey(PostUpload, on_delete=models.CASCADE, related_name="postsview")
    is_view = models.PositiveIntegerField(default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.post.post


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="postlike")
    post = models.ForeignKey(PostUpload, on_delete=models.CASCADE, related_name="postlike")
    is_like = models.PositiveIntegerField(default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.post


class PostShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="postshare")
    post = models.ForeignKey(PostUpload, on_delete=models.CASCADE,related_name="postshare")
    is_share = models.PositiveIntegerField(default=0, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.post.post
#
# class UserPost(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userposts")
#     title = models.CharField(max_length=255, blank=True, null=True, default="usertitle")
#     message = models.TextField(default="messages", blank=True, null=True)
#     post = models.TextField( blank=True, null=True)
#     uploadvideo = models.TextField( blank=True, null=True)
#
#     create_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user.email
#
# class UserPostLike(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userpostlike")
#     post = models.ForeignKey(UserPost, on_delete=models.CASCADE,related_name="userpostlike")
#     is_like = models.PositiveIntegerField(default=0, blank=True, null=True)
#     create_at = models.DateTimeField(auto_now_add=True)
#
# class UserPostsLike(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="newuserposts")
#     post = models.ForeignKey(UserPost, on_delete=models.CASCADE,related_name="usernewposts")
#     is_like = models.PositiveIntegerField(default=0, blank=True, null=True)
#     create_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.post