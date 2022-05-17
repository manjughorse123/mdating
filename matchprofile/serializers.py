
from requests import request
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from account.models import *
from account.serializers import *
from friend.models import FriendRequest
from .models import *
from usermedia.models import *
from usermedia.serializers import *
from friend.models import *


class genderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'


class UserfilterSerializerss(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'gender', 'birth_date', 'city',
                  'passion', 'idealmatch', 'name', 'image')


class UserMatchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMatchProfile
        fields = '__all__'


class GetUserMatchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMatchProfile
        fields = '__all__'

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['user'] = UserFriendSerializer(instance.user).data
    #     response['like_profile_user'] = UserFriendSerializer(
    #         instance.like_profile_user).data

    #     return response


class UserFilterSerializer(GeoFeatureModelSerializer):
    media = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    is_friend_req = serializers.SerializerMethodField()
    is_friend_acc = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    def get_age(self, obj):
        # age = User.calculate_age(obj.birth_date)
        age = User.objects.raw(
            "SELECT id, date_part('year', age(%s))::int as age  FROM account_user where id= %s", [obj.birth_date, obj.id])

        return age[0].age

    def get_media(self, obj):

        # user = self.context['request'].user
        medias_data = MediaPost.objects.filter(user=obj.id)
        media_data = GetMediaPostSerializers(medias_data, many=True)

        return media_data.data

    def get_is_friend_req(self, obj):

        user = self.context['request'].user
        friend_data = FriendRequest.objects.filter(user=user, friend=obj.id)
        if friend_data:
            return True
        else:
            return False

    def get_is_friend_acc(self, obj):

        user = self.context['request'].user
        friend_data = FriendList.objects.filter(user=user, friends=obj.id)
        if friend_data:
            return True
        else:
            return False

    def get_is_following(self, obj):

        user = self.context['request'].user
        is_following = FollowRequest.objects.filter(user=user, follow=obj.id)
        if is_following:
            return True
        else:
            return False

    class Meta:
        model = User
        geo_field = "location"
        fields = ('id',
                  'gender',
                  'birth_date',
                  'location',
                  'passion',
                  'idealmatch',
                  'name',
                  'image',
                  'address',
                  'city',
                  'marital_status',
                  'interest_in',
                  'media',
                  'age',
                  'is_friend_req',
                  'is_friend_acc',
                  'is_following'
                  )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['gender'] = genderSerializer(instance.gender).data
        response['interest_in'] = genderSerializer(instance.interest_in).data
        return response


# UserSeachFilterSerializer
class UserSeachFilterSerializer(serializers.ModelSerializer):

    is_friend_req = serializers.SerializerMethodField()
    is_friend_acc = serializers.SerializerMethodField()
    is_friend_get = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        age = User.calculate_age(obj.birth_date)

        return age

    def get_is_friend_req(self, obj):

        user = self.context['request'].user
        friend_data = FriendRequest.objects.filter(user=user, friend=obj.id)
        if friend_data:
            return True
        else:
            return False

    def get_is_friend_acc(self, obj):

        user = self.context['request'].user
        friend_data = FriendList.objects.filter(user=user, friends=obj.id)

        if friend_data:
            return True
        else:
            return False

    def get_is_friend_get(self, obj):

        user = self.context['request'].user
        friend_data = FriendRequest.objects.filter(
            user=obj.id, friend=user)
        if friend_data:
            return True
        else:
            return False

    class Meta:
        model = User

        fields = ('id',
                  'gender',
                  'birth_date',
                  'city',
                  'passion',
                  'idealmatch',
                  'name',
                  'image',
                  'is_friend_req',
                  'is_friend_acc',
                  'is_friend_get',
                  'age')
