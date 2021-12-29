from __future__ import unicode_literals

import datetime

from django.contrib.admin import options
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.expressions import RawSQL
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField
# https://pypi.org/project/django-ckeditor/
import random
import os
import requests

# Create your models here.
from rest_framework.fields import MultipleChoiceField


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError("Please enter correct password")
        user_obj = self.model(
            phone=phone
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,

        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,

        )
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number must be entered in the format: '+91-999999999'. Up to 14 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=20)
    standard = models.CharField(max_length=3, blank=True, null=True)
    score = models.IntegerField(default=16)
    first_login = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


def upload_image_path_profile(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext



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

class UserMedia(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    media = models.FileField(upload_to=upload_image_path_profile, default=None, null=True, blank=True)
    mediades = models.CharField(max_length=100, default="this is images")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class UserInterest(models.Model):
    interest = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.interest

class UserIdeaMatch(models.Model):
    ideamatch = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ideamatch

class RelationshipStatus(models.Model):
    relationship_status = models.CharField(max_length=200)
    slug = models.SlugField(max_length=5000)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.relationship_status

class Education(models.Model):
    educations = models.CharField(max_length=200)
    slug = models.SlugField(max_length=5000)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.educations

class BodyType(models.Model):
    body_type = models.CharField(max_length=200)
    slug = models.SlugField(max_length=5000)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body_type

class IsVerified(models.Model):
    is_verified = models.CharField(max_length=200)
    slug = models.SlugField(max_length=5000)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.is_verified

class Gender(models.Model):
    gender = models.CharField(max_length=100)
    slug = models.SlugField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gender


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = RichTextField()

    ideamatch = models.ManyToManyField(UserIdeaMatch)
    usermedia = models.ManyToManyField(UserMedia)
    userinterest = models.ManyToManyField(UserInterest)
    relationship_status = models.ManyToManyField(RelationshipStatus)
    education = models.ManyToManyField(Education)
    body_type = models.ManyToManyField(BodyType)
    is_verified = models.ForeignKey(IsVerified, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

    email = models.EmailField(blank=True, null=True)
    birth_date = models.DateField(null=True, default='1999-12-15', blank=True)
    height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2)
    location = models.CharField(max_length=100, default='', blank=False)
    citylat = models.DecimalField(max_digits=9, decimal_places=6, default='-2.0180319')
    citylong = models.DecimalField(max_digits=9, decimal_places=6, default='52.5525525')
    image = models.ImageField(upload_to='profile/', default=None, null=True, blank=True)
    address = models.CharField(max_length=900, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    first_count = models.IntegerField(default=0,
                                      help_text='It is 0, if the user is totally new and 1 if the user has saved his '
                                                'standard once')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    objects = LocationManager()

    # Assistance from https://stackoverflow.com/questions/5056327/define-and-insert-age-in-django-template
    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25)

    def __str__(self):
        return str(self.user)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(user_created_receiver, sender=User)


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number must be entered in the format: '+91-999999999'. Up to 14 "
                                         "digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of otp sent')
    logged = models.BooleanField(default=False, help_text='If otp verification got successful')
    forgot = models.BooleanField(default=False, help_text='only true for forgot password')
    forgot_logged = models.BooleanField(default=False, help_text='Only true if validdate otp forgot get successful')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
