from .models import *
from rest_framework import serializers

class UserVerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model  = UserVerification
        fields = '__all__'


class AdminUserVerifiedSerializer(serializers.ModelSerializer):

    class Meta:
        model  = AdminUserVerified
        fields = '__all__'