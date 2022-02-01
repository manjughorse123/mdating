from .models import *
from rest_framework import serializers


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


class UserMatchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMatchProfile
        fields = '__all__'
