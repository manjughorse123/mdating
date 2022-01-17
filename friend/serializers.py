from .models import *
from rest_framework import serializers


class FriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendList
        fields = "__all__"