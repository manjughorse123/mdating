from django.contrib.auth import get_user_model
from rest_framework.serializers import *
from rest_framework import serializers
from .models import *
from account.models import *
from rest_framework.fields import SerializerMethodField


class PostUploadCreateSerializers(ModelSerializer):
    # is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = PostUpload
        fields = '__all__'



    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserFriendSerilaizer(instance.user).data

        return response

class PostUploadSerializers(ModelSerializer):
    # is_liked = serializers.BooleanField(read_only=True)
    # isLiked = serializers.SerializerMethodField()
    # isViewed = serializers.SerializerMethodField()
    class Meta:
        model = PostUpload
        fields = '__all__'




class PostUploadV2Serializers(ModelSerializer):
    # is_liked = serializers.BooleanField(read_only=True)
    isLiked = serializers.SerializerMethodField()
    isViewed = serializers.SerializerMethodField()
    class Meta:
        model = PostUpload
        fields = ('user','post','title', 'is_like_count','is_view_count','isLiked','isViewed')

    def get_isLiked(self, obj):
        requestUser = self.context['request'].user
        return PostLike.objects.filter(post=obj, user=requestUser).exists()

    def get_isViewed(self, obj):
        requestUser = self.context['request'].user
        return PostView.objects.filter(post=obj, user=requestUser).exists()


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserFriendSerilaizer(instance.user).data

        return response

class UserFriendSerilaizer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name','image','email')


class UserPostUpdateSerilaizer(ModelSerializer):
    class Meta:
        model = PostUpload
        fields = '__all__'


class PostViewSerializers(ModelSerializer):
    class Meta:
        model = PostView
        fields = "__all__"

        # def to_representation(self, instance):
        #     response = super().to_representation(instance)
        #     response['user'] = UserFriendSerilaizer(instance.user).data
        #     # response['post'] = UserPostUpdateSerilaizer(instance.post).data
        #
        #     return response


class PostLikeSerializers(ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserFriendSerilaizer(instance.user).data
        response['post'] = UserPostUpdateSerilaizer(instance.post).data

        return response


class PostShareSerializers(ModelSerializer):
    class Meta:
        model = PostShare
        fields = "__all__"

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['user'] = UserFriendSerilaizer(instance.user).data
    #     response['post'] = UserPostUpdateSerilaizer(instance.post).data
    #
    #     return response


# class UserPostLikeSerializers(ModelSerializer):
#     class Meta:
#         model = UserPostLike
#         fields = "__all__"
#
# class UserPostSerializers(ModelSerializer):
#     post_like = UserPostLikeSerializers()
#
#     class Meta:
#         model = UserPost
#         fields = ('post','title','post_like','message',)


class PostUploadUpdateSerializers(ModelSerializer):

    class Meta:
        model = PostUpload
        fields = ('post','title', 'message',)
