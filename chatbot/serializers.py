import imp
from rest_framework import serializers
from .models import *
from account.models import *

class UserProfileDataSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ('name','email','id','profile_image')

class UserChatSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ChatList
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sender'] = UserProfileDataSerializer(instance.sender).data

        response['receiver'] = UserProfileDataSerializer(instance.receiver).data
        
    
        return response

class UserChatNewSerializer(serializers.ModelSerializer):
    count_un_read = serializers.SerializerMethodField()
    def get_count_un_read(self, obj):
        
        user = self.context['request']
        user_data = User.objects.get(
            id=user)
        # user_data2 = User.objects.get(
        #     id=obj.receiver.id)
        
        user_data2 = User.objects.get(
            id=obj.sender.id)
        userChatReadValue =ChatList.objects.filter(receiver=user_data,sender=user_data2,is_text_read=False).exclude(is_text= "")
        # userChatReadValue =ChatList.objects.filter(receiver=user_data2,sender=user_data,is_text_read=False).exclude(is_text= "")
        
            
        return len(userChatReadValue)
   
    class Meta:
        model = ChatList
        fields = ('id','sender','create_at','receiver','count_un_read','is_text',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sender'] = UserProfileDataSerializer(instance.sender).data

        response['receiver'] = UserProfileDataSerializer(instance.receiver).data
        
    
        return response

