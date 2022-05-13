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

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['user'] = UserFriendSerializer(instance.user).data

    #     return response


class PostUploadSerializers(ModelSerializer):
    # is_liked = serializers.BooleanField(read_only=True)
    # isLiked = serializers.SerializerMethodField()
    # isViewed = serializers.SerializerMethodField()
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
                  'is_private')

    def get_isLiked(self, obj):

        requestUser = self.context['request'].user
        if PostLike.objects.filter(post=obj, user=requestUser, is_like=True).exists():

            return PostLike.objects.filter(post=obj, user=requestUser, is_like=True).exists()
        else:
            return PostLike.objects.filter(post=obj, user=requestUser, is_like=True).exists()

    # def get_isViewed(self, obj):
    #     requestUser = self.context['request'].user
    #     return PostView.objects.filter(post=obj, user=requestUser).exists()

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
                  'email')


class UserPostUpdateSerilaizer(ModelSerializer):
    class Meta:
        model = PostUpload
        fields = '__all__'


class NewPostUploadSerializers(ModelSerializer):
    class Meta:
        model = PostUpload
        fields = ('post', 'message', 'title',)


class PostViewSerializers(ModelSerializer):
    class Meta:
        model = PostView
        fields = ('post',)

        # def to_representation(self, instance):
        #     response = super().to_representation(instance)
        #     response['user'] = UserFriendSerializer(instance.user).data
        #     # response['post'] = UserPostUpdateSerilaizer(instance.post).data
        #
        #     return response


class PostLikeSerializers(ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('post',)

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['user'] = UserFriendSerializer(instance.user).data
    #     response['post'] = UserPostUpdateSerilaizer(instance.post).data

    #     return response


class PostShareSerializers(ModelSerializer):
    class Meta:
        model = PostShare
        fields = ('post',)

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['user'] = UserFriendSerializer(instance.user).data
    #     response['post'] = UserPostUpdateSerilaizer(instance.post).data
    #
    #     return response


class PostUploadUpdateSerializers(ModelSerializer):

    class Meta:
        model = PostUpload
        fields = ('id', 'post', 'title', 'message',)


class PostReportsSerializers(ModelSerializer):

    class Meta:
        model = PostReport
        fields = '__all__'
