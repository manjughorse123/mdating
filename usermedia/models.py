from django.db import models
from account.models import *
# Create your models here.

MAYBECHOICE = (
    (0, 'all'),
    (1, 'friend'),
    (2, 'onlyme'),
)


class MediaPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=300, null=True, blank=True)
    media = models.TextField(max_length=500, null=True, blank=True)
    media_video = models.TextField(max_length=500, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    like_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    share_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    # is_media = models.BooleanField(default=False)
    media_report = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    show_media_photo = models.IntegerField(
        choices=MAYBECHOICE, default=2)

    def __str__(self):
        return str(self.media)


class MediaVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_caption = models.CharField(max_length=300, null=True, blank=True)
    media_video = models.TextField(max_length=500, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    like_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    # is_media = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    show_media_video = models.IntegerField(
        choices=MAYBECHOICE, default=2)

    def __str__(self):
        return str(self.user.name)


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


class MediaPostReport(models.Model):

    report_text = models.CharField(max_length=300, null=True, blank=True)
    media = models.TextField(max_length=500, null=True, blank=True)
    media_post = models.ForeignKey(MediaPost, on_delete=models.CASCADE)
    # is_media = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.media_post)
