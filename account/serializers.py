
from rest_framework import serializers

from account.models import *


class PassionSerializer(serializers.ModelSerializer):
    passion = serializers.CharField(max_length=100)

    class Meta:
        model = Passion
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):

        model = User
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['gender'] = GenderSerializer(instance.gender).data

        response['interest_in'] = GenderSerializer(instance.interest_in).data
        response['tall'] = HeightSerializer(instance.tall).data
        response['marital_status'] = MaritalStatusSerializer(
            instance.marital_status).data

        return response


class UserProfileSerializer(serializers.ModelSerializer):
    user_passion = serializers.SerializerMethodField()
    user_idealmatch = serializers.SerializerMethodField()

    def get_user_passion(self, obj):
        if (obj.passion.count()) > 0:
            splitlist1 = obj.passion.all()
            user_passion = PassionSerializer(splitlist1, many=True)
            # user_passion = ",".join([str(i.passion) for i in splitlist1])
            return user_passion.data
        else:
            return "-"

    def get_user_idealmatch(self, obj):
        if (obj.idealmatch.count()) > 0:
            splitlist1 = obj.idealmatch.all()
            user_idealmatch = IdealMatchSerializer(splitlist1, many=True)
            return user_idealmatch.data
        else:
            return "-"

    class Meta(object):

        model = User
        fields = ('name', 'id', 'gender', 'passion', 'country_code', 'mobile', 'birth_date', 'image', 'bio', 'about',
                  'interest_in', 'tall', 'marital_status', 'idealmatch', 'email', 'user_passion', 'user_idealmatch', 'city', 'location',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['gender'] = GenderSerializer(instance.gender).data

        response['interest_in'] = GenderSerializer(instance.interest_in).data
        response['tall'] = HeightSerializer(instance.tall).data
        response['marital_status'] = MaritalStatusSerializer(
            instance.marital_status).data

        return response


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for Regiter User endpoint.
    """
    email = serializers.EmailField(
        required=True,
    )

    def validate(self, attrs):

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
        fields = ('id', 'is_gender', 'is_passion', 'is_tall', 'is_location',
                  'is_interest_in', 'is_idealmatch', 'is_marital_status', 'is_media', 'is_complete_profile',)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login
    """

    class Meta:
        model = User
        fields = ('mobile', 'country_code', 'otp')


class UserOtpSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login
    """

    class Meta:
        model = User
        fields = ('mobile', 'country_code')


class UserGenderSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login
    """

    class Meta:
        model = User
        fields = ('gender',)
        read_only_fields = ('id', 'email', 'name', 'mobile',)


class UserVerifiedSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'is_register_user_verified')


class UserVerifyDocSerializer(serializers.ModelSerializer):
    govt_id = serializers.CharField(max_length=200)
    selfie = serializers.CharField(max_length=200)

    class Meta:

        model = User
        fields = ('id', 'govt_id', 'selfie')


class UserResendOtpSerializer(serializers.ModelSerializer):
    govt_id = serializers.CharField(max_length=200)
    selfie = serializers.CharField(max_length=200)

    class Meta:

        model = User
        fields = ('id', 'govt_id', 'selfie')
