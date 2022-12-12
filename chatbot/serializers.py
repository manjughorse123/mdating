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
        # import pdb;pdb.set_trace()
        user = self.context['request']
        user_data = User.objects.get(
            id=user)
            
        userChatReadValue =ChatList.objects.filter(receiver=user_data,is_text_read=False)
        
            
        return len(userChatReadValue)
   
    class Meta:
        model = ChatList
        fields = ('id','sender','create_at','receiver','count_un_read',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sender'] = UserProfileDataSerializer(instance.sender).data

        response['receiver'] = UserProfileDataSerializer(instance.receiver).data
        
    
        return response

