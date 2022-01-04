import uuid
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


# from django.contrib.auth.models import User

class User(AbstractBaseUser):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=500, unique=True)
    name = models.CharField(max_length=200)
    birth_date = models.DateField(default='1999-12-15')
    mobile = models.CharField(max_length=10)
    country_code = models.CharField(max_length=8)
    otp = models.CharField(max_length=4)
    # is_activate = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    username = None
    password = None
    last_login = None

    USERNAME_FIELD = 'mobile'

    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25)
