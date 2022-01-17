import uuid
from datetime import datetime
import random
import os
from django.db.models.base import Model

from django.db.models.deletion import CASCADE
from ckeditor.fields import RichTextField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.expressions import RawSQL
from rest_framework.authtoken.models import Token


class LocationManager(models.Manager):

    # Assistance from https://stackoverflow.com/questions/19703975/django-sort-by-distance
    def nearby_locations(self, citylat, citylong, max_distance=None):
        """
        Return objects sorted by distance to specified coordinates
        which distance is less than max_distance given in kilometers
        """
        gcd_formula = "6371 * acos(cos(radians(%s)) * \
        cos(radians(citylat)) \
        * cos(radians(citylong) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(citylat)))"
        distance_raw_sql = RawSQL(
            gcd_formula,
            (citylat, citylong, citylat)
        )

        if max_distance is not None:
            return self.annotate(distance=distance_raw_sql).filter(distance__lt=max_distance)
        else:
            return self.annotate(distance=distance_raw_sql)


# class UserMedia(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
#     image = models.URLField(blank=True, null=True)
    
#     create_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

class Interest(models.Model):
    interest = models.CharField(max_length=40,unique = True)
    icon = models.URLField(blank=True, null=True)
    icon_color = models.CharField(max_length=40)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.interest)


class IdealMatch(models.Model):
    idealmatch = models.CharField(max_length=40,unique = True)
    icon = models.URLField(blank=True, null=True)
    icon_color = models.CharField(max_length=40)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.idealmatch)



class Gender(models.Model):
    gender = models.CharField(max_length=40, unique = True)
    icon = models.URLField(blank=True, null=True)
    icon_color = models.CharField(max_length=40)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gender

class MaritalStatus(models.Model):
    status = models.CharField(max_length=40, unique = True)
    icon = models.URLField(blank=True, null=True)
    icon_color = models.CharField(max_length=40)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

class User(AbstractBaseUser):
    id = models.UUIDField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=500, unique=True, blank=True, null=True)
    mobile = models.CharField(max_length=10, unique=True, blank=True, null=True)
    country_code = models.CharField(max_length=8, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    bio = RichTextField(blank=True, null=True)
    birth_date = models.DateField(default='1999-12-15')
    otp = models.CharField(max_length=4, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    username = None
    password = None
    last_login = None

    relationship_status = models.ForeignKey(MaritalStatus,on_delete=models.CASCADE ,related_name='user_merital_status',blank=True, null=True)
    education = models.CharField(max_length=50, blank=True, null=True)
    body_type = models.CharField(max_length=50, blank=True, null=True)
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE, related_name='user_gender',blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2, blank=True, null=True)
    location = models.CharField(max_length=100, default='', blank=True, null=True)
    citylat = models.DecimalField(max_digits=9, decimal_places=6, default='-2.0180319', blank=True, null=True)
    citylong = models.DecimalField(max_digits=9, decimal_places=6, default='52.5525525', blank=True, null=True)
    address = models.CharField(max_length=900, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False, blank=True, null=True)
    first_count = models.IntegerField(default=0,
                                      help_text='It is 0, if the user is totally new and 1 if the user has saved his '
                                                'standard once', blank=True, null=True)

    # create_at = models.DateTimeField(auto_now_add=True)
    # update_at = models.DateTimeField(auto_now=True)
    # objects = LocationManager()

    USERNAME_FIELD = 'mobile'

    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25)

    def __str__(self):
        return str(self.email)

class UserMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name= 'user_image_profile') 
    title =  models.CharField(max_length = 255,blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserIdealMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name= 'user_ideal')
    idealmatch = models.ForeignKey(IdealMatch, on_delete=models.CASCADE , related_name= 'user_match')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.idealmatch)+','+str(self.user.name)

class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name= 'user_inter')
    # interest = models.ForeignKey(Interest, on_delete=models.CASCADE , related_name= 'user_interest')
    interest = models.ManyToManyField(Interest,  related_name= 'user_interest')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.interest)+','+str(self.user.name)


class ProfileCount(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name= 'user_profile_count')
    viewcount = models.IntegerField(default=0)
    