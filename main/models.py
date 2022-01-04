from __future__ import unicode_literals
import datetime
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

from account.models import *

# Create your models here.



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
    media = models.FileField(upload_to=upload_image_path_profile, default=None, null=True, blank=True)
    mediades = models.CharField(max_length=100, default="this is images")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class Gender(models.Model):
    gender = models.CharField(max_length=100)
    slug = models.SlugField(max_length=500)
    icon = models.ImageField(upload_to="gender/")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gender


class UserInterest(models.Model):
    interest = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    icon = models.ImageField(upload_to="interest/")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.interest


class UserIdeaMatch(models.Model):
    ideamatch = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    icon = models.ImageField(upload_to="ideamatch/")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ideamatch


class RelationshipStatus(models.Model):
    relationship_status = models.CharField(max_length=200)
    slug = models.SlugField(max_length=5000)
    icon = models.ImageField(upload_to="relations/")
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




class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = RichTextField()

    ideamatch = models.ManyToManyField(UserIdeaMatch)
    usermedia = models.ManyToManyField(UserMedia)
    userinterest = models.ManyToManyField(UserInterest)
    relationship_status = models.ManyToManyField(RelationshipStatus)
    education = models.ManyToManyField(Education)
    body_type = models.ManyToManyField(BodyType)
    is_verified = models.ForeignKey(IsVerified, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

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


    def __str__(self):
        return str(self.user)

#
# def user_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         Profile.objects.get_or_create(user=instance)
#
#
# post_save.connect(user_created_receiver, sender=User)

