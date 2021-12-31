from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# from django.contrib.auth.models import User

class User(AbstractBaseUser):
    email = models.EmailField(max_length=500, unique=True)
    name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, default='1999-12-15', blank=True)
    mobile = models.CharField(max_length=14)
    country_code = models.CharField(max_length=8)
    otp = models.CharField(max_length=6)

    password = None
    last_login = None
    create_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25)


