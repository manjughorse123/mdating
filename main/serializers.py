from rest_framework import serializers
from .models import *


class UserMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMedia
        fields = "__all__"


class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = "__all__"


class UserIdeaMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIdeaMatch
        fields = "__all__"


class RelationshipStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationshipStatus
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class BodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = "__all__"


class IsVerifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsVerified
        fields = "__all__"


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
