import imp
from rest_framework import serializers
from .models import *
from account.models import *

class UserProfileDataSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ('name','email','id',)

class UserChatSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ChatList
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sender'] = UserProfileDataSerializer(instance.sender).data

        response['receiver'] = UserProfileDataSerializer(instance.receiver).data
        
    
        return response