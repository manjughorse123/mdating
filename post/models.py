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
    user_post  = models.ImageField(upload_to='user_post_image/',blank=True, null=True)
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
        choices=MAYBECHOICE, default=2)
    is_soft_delete = models.BooleanField(
        default=False, blank=True, null=True)

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
        return str(self.post.post)


class PostLike(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="postlike")
    post = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="postlike")
    is_like = models.BooleanField(blank=True, null=True, default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post.post)


# class PostShare(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="postshare")
#     post = models.ForeignKey(
#         PostUpload, on_delete=models.CASCADE, related_name="postshare")
#     is_share = models.PositiveIntegerField(default=0, blank=True, null=True)
#     create_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.post.post




class PostImageUpload(models.Model):
    post_image = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="userpostiamge")
    user_post_image = models.ImageField(upload_to='user_post_image/',blank=True, null=True)
    user_post_video = models.ImageField(upload_to='user_post_video/',blank=True, null=True)
    user_post_type = models.CharField(max_length= 255,blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    # update_at  = models.DateTimeField(now_add=True)

    def __str__(self):
        return str(self.id)


class PostReport(models.Model):

    post = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="postreplike",null=True,blank=True)
    report_text = models.CharField(max_length=255, blank=True, null=True,)
    # report_user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="reposrtuserpost",null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post.post)


class NewPostReport(models.Model):

    post = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="newpostreplike",null=True,blank=True)
    report_text = models.CharField(max_length=255, blank=True, null=True,)
    report_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="newreposrtuserpost",null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    is_report = models.BooleanField(default=True)
    repost_text = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.post.post)

# class NewPostReportReslove(models.Model):

#     post = models.ForeignKey(
#         PostUpload, on_delete=models.CASCADE, related_name="newpostrepost",null=True,blank=True)
#     repost_text = models.CharField(max_length=255, blank=True, null=True,)
#     post_user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="newrepostuserpost",null=True,blank=True)
#     create_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.post.post)


class PostImage(models.Model):

    post = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="postimages")
    post_image = models.CharField(max_length=255, blank=True, null=True,)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post.post)
