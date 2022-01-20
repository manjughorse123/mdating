from rest_framework.serializers import *
from .models import *


class MediaPostSerializers(ModelSerializer):
    class Meta:
        model = MediaPost
        fields = "__all__"


class MediaViewSerializers(ModelSerializer):
    class Meta:
        model = MediaView
        fields = "__all__"


class MediaLikeSerializers(ModelSerializer):
    class Meta:
        model = MediaLike
        fields = "__all__"


class MediaShareSerializers(ModelSerializer):
    class Meta:
        model = MediaShare
        fields = "__all__"
