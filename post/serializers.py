from django.contrib.auth import get_user_model
from rest_framework.serializers import *
from .models import *
from account.models import User
from rest_framework.fields import SerializerMethodField


class PostUploadSerializers(ModelSerializer):
    class Meta:
        model = PostUpload
        fields = '__all__'


class PostViewSerializers(ModelSerializer):
    class Meta:
        model = PostView
        fields = "__all__"


class PostLikeSerializers(ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"


class PostShareSerializers(ModelSerializer):
    class Meta:
        model = PostShare
        fields = "__all__"



