from django.db import models
from account.models import *
# Create your models here.
from fcm_django.models import AbstractFCMDevice
from django.db import models

class CusztomFCMDevice(AbstractFCMDevice):

    user = models.ForeignKey(User,on_delete=models.CASCADE ,blank=True, null=True, related_name = "fcm_user_id")
        