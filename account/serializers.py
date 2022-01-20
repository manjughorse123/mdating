
from enum import unique

from django.urls import exceptions
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for Regiter User endpoint.
    """
    email = serializers.EmailField(
        required=True,
    )

    password = serializers.CharField(write_only=True, required=True)
    confrim_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confrim_password']:

            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        if int(attrs['mobile']) < 10:

            raise serializers.ValidationError(
                {"Mobile no": "no  should be  10 digit."})

        return attrs

    def create(self, validated_data):

        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


class PassionSerializer(serializers.ModelSerializer):
    passion = serializers.CharField(max_length=100)
    icon = serializers.ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = Passion
        fields = "__all__"


class GenderSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(max_length=200)
    icon = serializers.ImageField(
        max_length=None, use_url=True,
    )
    icon = serializers.CharField(max_length=100)

    class Meta:
        model = Gender
        fields = "__all__"


class IdealMatchSerializer(serializers.ModelSerializer):
    idealmatch = serializers.CharField(max_length=200)
    icon = serializers.ImageField(
        max_length=None, use_url=True,
    )
    icon = serializers.CharField(max_length=100)

    class Meta:
        model = IdealMatch
        fields = "__all__"


class MaritalStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=200)
    icon = serializers.ImageField(
        max_length=None, use_url=True,
    )
    icon = serializers.CharField(max_length=100)

    class Meta:
        model = MaritalStatus
        fields = "__all__"


class UserMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMedia
        fields = ('id','user','image',)


class UserImageSerializer(serializers.ModelSerializer):
    images = UserMediaSerializer(many=True)

    # def create(self, validated_data):
    #     import pdb;pdb.set_trace()
    #     images_data = validated_data.pop('Prices')
    #     user = User.objects.create(**validated_data)
    #     for image_data in images_data:
    #         UserMedia.objects.create(user=user, **image_data)
    #     return user

    class Meta:
        model = User
        fields ='__all__'

# class UserMediaSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = UserMedia
#         fields = "__all__"


class UserIdealMatchSerializer(serializers.ModelSerializer):
    """
    Serializer for User Ideal Match
    """

    class Meta:
        model = UserIdealMatch
        fields = '__all__'



class UserPassionSerializer(serializers.ModelSerializer):
    
    """
    Serializer for User UserPassion
    """
    class Meta:
        model = UserPassion
        fields = ('user','passion')

    # def create(self, validated_data):
    #     passion = validated_data.pop('passion')
    #     user_inter = Userpassion.objects.create( **validated_data)
    #     user_inter.passion.add(*passion)
    #     return user_inter