from django.contrib.auth import get_user_model
from rest_framework.serializers import *
from .models import *
from account.models import User
from rest_framework.fields import SerializerMethodField


class PostUploadSerializers(ModelSerializer):
    class Meta:
        model = PostUpload
        fields = '__all__'


class PostReactionSerializers(ModelSerializer):
    class Meta:
        model = PostReaction
        fields = "__all__"


class MediaPostSerializers(ModelSerializer):
    class Meta:
        model = MediaPost
        fields = "__all__"


class MediaReactionSerializers(ModelSerializer):
    class Meta:
        model = MediaReaction
        fields = "__all__"
