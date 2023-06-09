from django.db import models
from account.models import *
# Create your models here.
from fcm_django.models import AbstractFCMDevice
from django.db import models
from post.models import *
class CusztomFCMDevice(AbstractFCMDevice):

    user = models.ForeignKey(User,on_delete=models.CASCADE ,blank=True, null=True, related_name = "fcm_user_id")

    def __str__(self):
        return self.user.mobile

class NotificationData(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Notify_user")
    
    post = models.ForeignKey(
        PostUpload, on_delete=models.CASCADE, related_name="postsview_notification",null=True,blank=True)
    is_notification_read = models.BooleanField(default=False)
    notification_message = models.TextField(null=True,blank=True)
    notify_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Notify_anotheruser",null=True,blank=True)
    flag = models.CharField(max_length=255, null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(auto_now=True)


class PublicUrl(models.Model):

    name = models.CharField(max_length=255, null=True,blank=True)
    description = RichTextField(null=True,blank=True)
    remark = models.CharField(max_length=255, null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(auto_now=True)
    

