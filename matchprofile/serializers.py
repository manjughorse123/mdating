from .models import *
from rest_framework import serializers
from account.models import *


#
class UserPassionMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPassion
        fields = '__all__'


class UserPassionMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPassion
        fields = '__all__'


class UserfilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'location', 'gender', 'birth_date', 'email')


class UserToUserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToUserLike
        fields = '__all__'


class UserToUserUnLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToUserUnLike
        fields = '__all__'


class UserFriendSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name','image')

class UserMatchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMatchProfile
        fields = '__all__'



class GetUserMatchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMatchProfile
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserFriendSerilaizer(instance.user).data
        response['like_profile_user'] = UserFriendSerilaizer(instance.like_profile_user).data

        return response

