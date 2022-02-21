from enum import unique

from django.urls import exceptions
from .models import *
from rest_framework import serializers


class PassionAddSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Passion
        fields = ('id', 'passion')

    # def display_value(self, instance):
    #     return instance
    #
    # def to_representation(self, value):
    #     return str(value)
    #
    # def to_internal_value(self, data):
    #     return Passion.objects.get(passion=data)

    # class Meta:
    #     model = Passion
    #     fields = ('id', 'passion')


class UserSerializer(serializers.ModelSerializer):
    # passion = serializers.ListSerializer(child=serializers.CharField(), required=False)
    # passion = PassionAddSerializer(many=True, required=False)
    # passion = serializers.ListField(child=serializers.PrimaryKeyRelatedField(many=True, queryset=Passion.objects.all()))
    class Meta(object):
        model = User
        fields = "__all__"
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['gender'] = GenderSerializer(instance.gender).data

        # response['passion'] = PassionSerializer(instance.passion).data

        return response

    #
    # def create(self, validated_data):
    #     passions_data = validated_data.pop('passion', [])
    #     user = super(UserSerializer, self).create(validated_data)
    #     for passions_data in passions_data:
    #         user.phone_set.create(passion=passions_data['passion'])
    #     return user
    #
    # def update(self, instance, validated_data):
    #     passion_data = validated_data.pop('passion', [])
    #     user = super(UserSerializer, self).update(instance, validated_data)
    #     # delete old
    #     user.passion.exclude(passion__in=[p['passion'] for p in passion_data]).delete()
    #     # create new
    #     for pass_data in passion_data:
    #         user.phone_set.get_or_create(passion=pass_data['passion'])
    #     return user

        # fields = ('passion',)
    #
    # def create(self, validated_data):
    #     passion = validated_data.pop('passion', [])
    #     movie = super().create(validated_data)
    #     passion_qs = Passion.objects.filter(passion__in=passion)
    #     movie.passion.add(*passion_qs)
    #     return movie

    # def validate(self, data):
    #     passion = data.get('genre', [])
    #     genre_obj_list = [Passion.objects.get(passion=passion) for passion in passion.all()]
    #     data.update({'genre': genre_obj_list})
    #     return data


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for Regiter User endpoint.
    """
    email = serializers.EmailField(
        required=True,
    )

    # password = serializers.CharField(write_only=True, required=True)
    # confrim_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        # if attrs['password'] != attrs['confrim_password']:
        #
        #
        #     raise serializers.ValidationError(
        #         {"password": "Password fields didn't match."})

        if int(attrs['mobile']) < 10:
            raise serializers.ValidationError(
                {"Mobile no": "no  should be  10 digit."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email']
        )

        # user.set_password(validated_data['password'])
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
        fields = ('id', 'user', 'image',)


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
        fields = '__all__'


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
        fields = ('user', 'passion')

    # def create(self, validated_data):
    #     passion = validated_data.pop('passion')
    #     user_inter = Userpassion.objects.create( **validated_data)
    #     user_inter.passion.add(*passion)
    #     return user_inter

class HeightSerializer(serializers.ModelSerializer):
    """
    Serializer for User Ideal Match
    """

    class Meta:
        model = Heigth
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for User Detail
    """

    class Meta:
        model = User
        fields = ('is_gender','is_passion','is_tall','is_location','is_interest_in','is_idealmatch','is_marital_status','is_media')


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login
    """

    class Meta:
        model = User
        fields = ('mobile','country_code','otp')

class UserOtpSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login
    """

    class Meta:
        model = User
        fields = ('mobile','country_code')


class UserGenderSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login
    """

    class Meta:
        model = User
        fields = ('gender',)
        read_only_fields = ('id','email','name','mobile',)