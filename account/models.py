from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# from django.contrib.auth.models import User

class User(AbstractBaseUser):
    email = models.EmailField(max_length=500, unique=True)
    name = models.CharField(max_length=200)
    password = None
    last_login = None
    create_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=14)
    otp = models.CharField(max_length=6)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mobile
