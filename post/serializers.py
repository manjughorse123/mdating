from django.contrib.auth import get_user_model
from rest_framework.serializers import *
from .models import *
from account.models import *
from rest_framework.fields import SerializerMethodField


class PostUploadSerializers(ModelSerializer):
    class Meta:
        model = PostUpload
        fields = '__all__'

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
        fields = ('id','user','post',)


class PostViewSerializers(ModelSerializer):
    class Meta:
        model = PostView
        fields = "__all__"

        # def to_representation(self, instance):
        #     response = super().to_representation(instance)
        #     response['user'] = UserFriendSerilaizer(instance.user).data
        #     response['post'] = UserPostUpdateSerilaizer(instance.post).data
        #
        #     return response


class PostLikeSerializers(ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['user'] = UserFriendSerilaizer(instance.user).data
    #     response['post'] = UserPostUpdateSerilaizer(instance.post).data
    #
    #     return response


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
