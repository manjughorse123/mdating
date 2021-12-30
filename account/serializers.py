from .models import *
from rest_framework import serializers


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
