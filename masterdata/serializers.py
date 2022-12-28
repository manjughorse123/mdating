from friend.models import *
from rest_framework import serializers
from .models import *
from account.models import * 

class UserProSerializer(serializers.ModelSerializer):

        class Meta:
            model  = User
            fields = ('id','name','email','profile_image',)

class FAQSerializer(serializers.ModelSerializer):

        class Meta:
            model  = FAQ
            fields = "__all__"


class NotificationDataSerializer(serializers.ModelSerializer):

    class Meta:
        model  = NotificationData
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserProSerializer(instance.user).data
        response['notify_user']= UserProSerializer(instance.notify_user).data
        return response
    
