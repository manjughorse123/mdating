from django.db import models
from account.models import *
# Create your models here.


class ChatList(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_sender")
    # friends = models.ManyToManyField(User, blank=True, related_name="friends")
    receiver = models.ForeignKey(
        User, blank=True, on_delete=models.CASCADE, related_name="user_receiver")
    is_text_read = models.BooleanField(default=False)
    is_text = models.TextField(null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    is_soft_delete = models.BooleanField(default=False)
  

    def __str__(self):
        return self.sender.name