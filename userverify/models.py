
from django.db import models
from account.models import *
# Create your models here.


class UserVerification(models.Model):

    user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_verified")
    selfy = models.CharField(max_length=255, null=True,blank=True)
    govt_id = models.CharField(max_length=255, null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.user.email


class AdminUserVerified(models.Model):
    user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_user_verified")
    is_verified = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.user.email