import uuid
from datetime import datetime
from colorfield.fields import ColorField
from django.db.models.base import Model
from ckeditor.fields import RichTextField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import RawSQL
from django.contrib.gis.db.models import *
from rest_framework.authtoken.models import Token


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

MAYBECHOICE = (
    (0, 'all'),
    (1, 'friend'),
    (2, 'onlyme'),
)
USERVERIFYCHOICE = (
    (0, 'panding'),
    (1, 'inprogress'),
    (2, 'verified'),
)


class User(AbstractBaseUser):
    id = models.UUIDField(max_length=100, primary_key=True,
                          default=uuid.uuid4, editable=False)
    email = models.EmailField(
        max_length=500, unique=True, blank=True, null=True)
    mobile = models.CharField(
        max_length=10, unique=True, blank=True, null=True)
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
    gender = models.ForeignKey(
        Gender, on_delete=models.CASCADE, related_name='user_gender', blank=True, null=True)
    is_gender = models.BooleanField(default=False)

    image = models.URLField(blank=True, null=True)
    profile_image =models.ImageField(upload_to='profile_image/',blank=True, null=True)
   
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

    idealmatch = models.ManyToManyField(
        IdealMatch, blank=True, db_column='IdealMatch')
    is_idealmatch = models.BooleanField(default=False)
    selfie = models.TextField( blank=True, null=True)
    selfie_url = models.ImageField(upload_to='selfie_image/',blank=True, null=True)
    govt_id = models.TextField( blank=True, null=True)
    govt_id_url =models.ImageField(upload_to='govt_id_image/',blank=True, null=True)
    is_govt_id_verified = models.BooleanField(default=False)
    is_register_user_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=8, blank=True, null=True)
    auth_tokens = models.TextField(blank=True, null=True)
    is_complete_profile = models.BooleanField(default=False)
    active_reseaon = models.TextField(blank=True, null=True)
    show_profile = models.IntegerField(
        choices=MAYBECHOICE, default=2)
    user_verified_status = models.IntegerField(
        choices=USERVERIFYCHOICE, default=0)    
    # objects = LocationManager()
    # objects = UserManager()
    USERNAME_FIELD = 'mobile'

    # def age(self):
    #     return int((datetime.date.today() - self.birth_date).days / 365.25)

    # def age(self):
    #     import datetime
    #     dob = self.birth_date
    #     tod = datetime.date.today()
    #     my_age = (tod.year - dob.year) - int((tod.month, tod.day) < (dob.month, dob.day))
    #     return my_age
    @classmethod
    def calculate_age(self, birth_date):
        import datetime
        return int((datetime.datetime.now().date() - birth_date).days / 365.25)

    # age = property(calculate_age)

    def __str__(self):
        return str(self.id)
