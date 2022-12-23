from django.contrib.auth import get_user_model
from rest_framework.serializers import *
from rest_framework import serializers
from .models import *
from account.models import *
from rest_framework.fields import SerializerMethodField
from friend.models import *


class PostUploadCreateSerializers(ModelSerializer):
    # is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = PostUpload
        fields = '__all__'

class PostUploadSerializers(ModelSerializer):
  
    class Meta:
        model = PostUpload
        fields = ('post',
                  'id',
                  'message',
                  'title',
                  'user',
                  'is_private',
                  'show_private_post',
                  'show_public_post')

class PostUploadUpdateSerializer(ModelSerializer):

  
    class Meta:
        model = PostUpload
        fields = ('post',
                  'id',
                  'message',
                  'title',
                  'user',
                  'is_private',
                  'show_private_post',
                  'show_public_post')


class PostUploadV2Serializers(ModelSerializer):
    # is_liked = serializers.BooleanField(read_only=True)
    isLiked = serializers.SerializerMethodField()
    # isViewed = serializers.SerializerMethodField()
    is_friend_req = serializers.SerializerMethodField()
    is_friend_acc = serializers.SerializerMethodField()
    is_friend_get = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()
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

    def get_is_friend_req(self, obj):

        user = self.context['request'].user
        friend_data = FriendRequest.objects.filter(user=user, friend=obj.user)
        if friend_data:
            return True
        else:
            return False

    def get_is_friend_acc(self, obj):

        user = self.context['request'].user
        friend_data = FriendList.objects.filter(user=user, friends=obj.user)
        if friend_data:
            return True
        else:
            return False

    def get_is_friend_get(self, obj):

        user = self.context['request'].user
        friend_data = FriendRequest.objects.filter(
            user=obj.user, friend=user)
        if friend_data:
            return True
        else:
            return False

    def get_is_user(self, obj):
        user = self.context['request'].user.id
        user_data = User.objects.get(
            id=user)
        user_datas = User.objects.get(
            id=obj.user.id)
        if user_data == user_datas:
            return True
        else:
            return False

    class Meta:
        model = PostUpload
        fields = ('id',
                  'user',
                  'post',
                  'title',
                  'message',
                  'is_like_count',
                  'is_user',
                  'is_friend_get',
                  'is_view_count',
                  'isLiked',
                  'post_report',
                  'is_friend_req',
                  'is_friend_acc',
                  'show_public_post',
                  'show_private_post',
                  'is_private',
                  'create_at',
                  'post_images',
                )

    def get_isLiked(self, obj):

        requestUser = self.context['request'].user
        if PostLike.objects.filter(post=obj, user=requestUser, is_like=True).exists():

            return PostLike.objects.filter(post=obj, user=requestUser, is_like=True).exists()
        else:
            return PostLike.objects.filter(post=obj, user=requestUser, is_like=True).exists()


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserFriendSerializer(instance.user).data

        return response


class UserFriendSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'name',
                  'image',
                  'profile_image',
                  'email',
                  'is_register_user_verified',)


class UserPostUpdateSerilaizer(ModelSerializer):
    class Meta:
        model = PostUpload
        fields = '__all__'


class NewPostUploadSerializers(ModelSerializer):
    class Meta:
        model = PostUpload
        fields = ('post', 'message', 'title',)

class PostImageUploadSerilaizer(ModelSerializer):
    class Meta:
        model = PostImageUpload
        fields = "__all__"
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['post_image'] = UserPostUpdateSerilaizer(instance.post_image).data

        return response

class PostViewSerializers(ModelSerializer):
    class Meta:
        model = PostView
        fields = ('post',)


class PostLikeSerializers(ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('post',)


class PostUploadUpdateSerializers(ModelSerializer):
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
        fields = ('id', 'post', 'title', 'message','post_images',)


class PostUploadVideoSerializers(ModelSerializer):
    post_images = serializers.SerializerMethodField()

    def get_post_images(self,obj):
        # import pdb;pdb.set_trace()
        post_images = []
        ad  = PostUpload.objects.filter(id = obj.id)
        for i in range(len(ad)):
            # user = User.objects.filter(id= ad[i].user.id)
            setData = PostImageUpload.objects.filter(post_image=ad[i],user_post_type='video/mp4')

            datas = PostImageUploadSerilaizer(setData,many= True)

            
        # return datas.data
        if len(setData) >0  :
            post_images.append(datas.data)
            print("manju",post_images)
            return datas.data
        else :
            return []

    class Meta:
        model = PostUpload
        fields = ('id', 'post', 'title', 'message','post_images',)



class PostReportsSerializers(ModelSerializer):

    class Meta:
        model = PostReport
        fields = '__all__'
