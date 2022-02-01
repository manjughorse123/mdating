from rest_framework.serializers import *
from account.models import *
from friend.models import *
from matchprofile.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class UserFilterSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = User
        geo_field = "location"
        fields = ('id', 'gender', 'birth_date', 'location')


class FollowRequestSerializer(ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = "__all__"


class FollowAcceptSerializer(ModelSerializer):
    class Meta:
        model = FollowAccept
        fields = "__all__"


class UserIdealMatchSerializer(ModelSerializer):
    class Meta:
        model = UserIdealMatch
        fields = ("user", 'idealmatch', 'create_at')


class UserPassionSerializer(ModelSerializer):
    class Meta:
        model = UserPassion
        fields = ("user", 'passion', 'create_at')


class UserMatchProfileFilterSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = UserMatchProfile
        fields = "__all__"


class NewUserMatchProfileFilterSerializer(ModelSerializer):
    class Meta:
        model = NewUserMatchProfile
        fields = "__all__"


