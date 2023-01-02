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

class PostImageUploadSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = PostImageUpload
        fields = ("id","user_post_image","user_post_type","create_at","post_image",)
    
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['post_image'] = UserPostUpdateSerilaizer(instance.post_image).data

    #     return response

class PostUploadV2Serializers(serializers.ModelSerializer):
   
    post_images = serializers.SerializerMethodField()

    def get_post_images(self,obj):
        setData = PostImageUpload.objects.filter(post_image=obj.id)
       
        datas = PostImageUploadSerilaizer(setData,many= True)
        print(datas.data)
        # return datas.data
        if datas :

            return datas.data
        else :
            return []

    class Meta:
        model = PostUpload
        fields = ('id',    
                  'post',
                  'title',
                  'message',            
                  'is_private',
                  'create_at',
                  'post_images',
                )




class NotificationDataSerializer(serializers.ModelSerializer):


    class Meta:
        model  = NotificationData
        fields = ('id','notification_message','user','notify_user','create_at','flag','post')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserProSerializer(instance.user).data
        response['notify_user']= UserProSerializer(instance.notify_user).data
        response['post']=PostUploadV2Serializers(instance.post).data

        return response
    
