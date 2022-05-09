from rest_framework.serializers import *
from rest_framework import serializers
from account.models import *
from friend.models import *
from matchprofile.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from datetime import date
from django.utils.timezone import now

class UserFilterSerializer(GeoFeatureModelSerializer):
# class FollowRequestSerializer(ModelSerializer):
#     age_range = serializers.SerializerMethodField()
#     min_age = serializers.IntegerField(required=True)
#     min_age = serializers.IntegerField(required=True)
#
#     def get_age_range(self  , obj):
#         current = now().date()
#         min_date = date(current.year - min_age, current.month, current.day)
#         max_date = date(current.year - max_age, current.month, current.day)
#
#         return User.objects.filter(birth_date__gte=max_date,
#                                birth_date__lte=min_date).order_by("birth_date")

    class Meta:
        model = User
        geo_field = "location"
        fields = ('id', 'gender', 'birth_date', 'location','passion','idealmatch','name','image')


class FollowRequestSerializer(ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = "__all__"


class FollowAcceptSerializer(ModelSerializer):
    class Meta:
        model = FollowAccept
        fields = "__all__"







class UserMatchProfileFilterSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = UserMatchProfile
        fields = "__all__"


class NewUserMatchProfileFilterSerializer(ModelSerializer):
    class Meta:
        model = NewUserMatchProfile
        fields = "__all__"


