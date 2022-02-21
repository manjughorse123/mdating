from pyexpat import model
import uuid
from datetime import datetime
import random
import os
from django.db.models.base import Model
from colorfield.fields import ColorField
from django.db.models.deletion import CASCADE
from ckeditor.fields import RichTextField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.expressions import RawSQL
from rest_framework.authtoken.models import Token
from django.contrib.gis.db.models import *


# class LocationManager(models.Manager):
#
#     # Assistance from https://stackoverflow.com/questions/19703975/django-sort-by-distance
#     def nearby_locations(self, citylat, citylong, max_distance=None):
#         """
#         Return objects sorted by distance to specified coordinates
#         which distance is less than max_distance given in kilometers
#         """
#         gcd_formula = "6371 * acos(cos(radians(%s)) * \
#         cos(radians(citylat)) \
#         * cos(radians(citylong) - radians(%s)) + \
#         sin(radians(%s)) * sin(radians(citylat)))"
#         distance_raw_sql = RawSQL(
#             gcd_formula,
#             (citylat, citylong, citylat)
#         )
#
#         if max_distance is not None:
#             return self.annotate(distance=distance_raw_sql).filter(distance__lt=max_distance)
#         else:
#             return self.annotate(distance=distance_raw_sql)
#

# class UserMedia(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE) 

#     image = models.URLField(blank=True, null=True)

#     create_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


class Passion(models.Model):
    passion = models.CharField(max_length=40, unique=True)
    slug_field = models.SlugField(max_length=220)
    icon = models.ImageField(upload_to='passion_icon/')
    icon_color = ColorField(format='hexa')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.passion)


class MasterTable(models.Model):

    name = models.CharField(max_length=40, unique=True)
    icon = models.ImageField(upload_to='idealMatch_icon/')
    icon_bg_color = ColorField(format='hexa')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name) 

class IdealMatch(models.Model):
    idealmatch = models.CharField(max_length=40, unique=True)
    icon = models.ImageField(upload_to='idealMatch_icon/')
    icon_color = ColorField(format='hexa')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.idealmatch)


class Gender(models.Model):
    gender = models.CharField(max_length=40, unique=True)
    icon = models.URLField(blank=True, null=True)
    icon = models.ImageField(upload_to='gender_icon/')
    icon_color = ColorField(format='hexa')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gender


class MaritalStatus(models.Model):
    status = models.CharField(max_length=40, unique=True)
    icon = models.ImageField(upload_to='maritalstatus_icon/')
    icon_color = ColorField(format='hexa')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

class Heigth(models.Model):

    height = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.height
from django.contrib.auth.models import UserManager
# class User(AbstractBaseUser):
#     id = models.UUIDField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
#     email = models.EmailField(max_length=500, unique=True, blank=True, null=True)
#     mobile = models.CharField(max_length=10, unique=True, blank=True, null=True)
#     country_code = models.CharField(max_length=8, blank=True, null=True)
#     name = models.CharField(max_length=200, blank=True, null=True)
#     bio = RichTextField(blank=True, null=True)
#     birth_date = models.DateField(default='1999-12-15')
#     otp = models.CharField(max_length=4, blank=True, null=True)
#     is_phone_verified = models.BooleanField(default=False)
#     username = None
#     password = None
#     last_login = None

#     is_media_field = models.BooleanField(default=False)

#     relationship_status = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE, related_name='user_merital_status',
#                                             blank=True, null=True)
#     relationship_status_field = models.BooleanField(default=False)

#     education = models.CharField(max_length=50, blank=True, null=True)
#     body_type = models.CharField(max_length=50, blank=True, null=True)

#     gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='user_gender', blank=True, null=True)
#     gender_field = models.BooleanField(default=False)

#     image = models.URLField(blank=True, null=True)

#     # height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2, blank=True, null=True)
#     height_field = models.BooleanField(default=False)
#     heights = models.ForeignKey(Heigth, on_delete=models.CASCADE, related_name='user_height',
#                                 blank=True, null=True)
#     location = PointField(srid=4326, blank=True, null=True)
#     address = models.CharField(max_length=100, blank=True, null=True)
#     city = models.CharField(max_length=50, blank=True, null=True)
#     location_field = models.BooleanField(default=False)

#     is_premium = models.BooleanField(default=False)
#     is_verified = models.BooleanField(default=False, blank=True, null=True)
#     # first_count = models.IntegerField(default=0,
#     #                                   help_text='It is 0, if the user is totally new and 1 if the user has saved his '
#     #                                             'standard once', blank=True, null=True)
#     about = models.TextField(blank=True, null=True)

#     interest_in = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='interest_in_gender', blank=True,
#                                     null=True)
#     interest_in_field = models.BooleanField(default=False)

#     passion = models.ManyToManyField(Passion, blank=True, db_column='passion')
#     passion_field = models.BooleanField(default=False)

#     idealmatch = models.ManyToManyField(IdealMatch, blank=True, db_column='IdealMatch' )
#     idealmatch_field = models.BooleanField(default=False)
#     # passion_in_field = models.BooleanField(default=False)
#     selfie = models.CharField(max_length=255, blank=True, null=True)
#     govt_id = models.CharField(max_length=255, blank=True, null=True)
#     is_govt_id_verified = models.BooleanField(default=False)
#     is_register_user_verified = models.BooleanField(default=False)
#     create_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)

#     # objects = LocationManager()
#     # objects = UserManager()
#     USERNAME_FIELD = 'mobile'

#     def age(self):
#         return int((datetime.date.today() - self.birth_date).days / 365.25)

#     def __str__(self):
#         return str(self.email)


#     def written_by(self):
#         return ",".join([str(p) for p in self.passion_in.all()])

class User(AbstractBaseUser):
    id = models.UUIDField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=500, unique=True, blank=True, null=True)
    mobile = models.CharField(max_length=10, unique=True, blank=True, null=True)
    country_code = models.CharField(max_length=8, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    bio = RichTextField(blank=True, null=True)
    birth_date = models.DateField(default='1999-12-15')
    otp = models.CharField(max_length=4, blank=True, null=True)
    username = None
    password = None
    last_login = None
    is_media = models.BooleanField(default=False)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE, related_name='user_merital_status',
                                            blank=True, null=True)
    is_marital_status = models.BooleanField(default=False)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='user_gender', blank=True, null=True)
    is_gender = models.BooleanField(default=False)

    image = models.URLField(blank=True, null=True)
    is_tall = models.BooleanField(default=False)
    tall = models.ForeignKey(Heigth, on_delete=models.CASCADE, related_name='user_height',
                                blank=True, null=True)
    location = PointField(srid=4326, blank=True, null=True)
    is_location = models.BooleanField(default=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    interest_in = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name='interest_in_gender', blank=True,
                                    null=True)
    is_interest_in = models.BooleanField(default=False)

    passion = models.ManyToManyField(Passion, blank=True, db_column='passion')
    is_passion = models.BooleanField(default=False)

    idealmatch = models.ManyToManyField(IdealMatch, blank=True, db_column='IdealMatch' )
    is_idealmatch = models.BooleanField(default=False)
    selfie = models.CharField(max_length=255, blank=True, null=True)
    govt_id = models.CharField(max_length=255, blank=True, null=True)
    is_govt_id_verified = models.BooleanField(default=False)
    is_register_user_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # objects = LocationManager()
    # objects = UserManager()
    USERNAME_FIELD = 'mobile'

    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25)

    def __str__(self):
        return str(self.email)


class UserMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_image_profile')
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserIdealMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ideal')
    idealmatch = models.ForeignKey(IdealMatch, on_delete=models.CASCADE, related_name='user_match')
    is_idealmatch = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    # idealmatch = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.idealmatch) + ',' + str(self.user.name)


class UserPassion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_inter')
    passion = models.ForeignKey(Passion, on_delete=models.CASCADE, related_name='user_Passion')
    is_Passion = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    # passion = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.passion) + ',' + str(self.user.name)

    def add_passion(self):
        return ",".join([str(p) for p in self.passion.all()])


