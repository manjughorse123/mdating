from .models import *
from rest_framework import serializers


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
