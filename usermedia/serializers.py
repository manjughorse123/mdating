from rest_framework.serializers import *
from rest_framework import serializers
from .models import *
from friend.models import *

# isLiked = serializers.SerializerMethodField()
#     isViewed = serializers.SerializerMethodField()
#     class Meta:
#         model = PostUpload
#         fields = ('user','post','title', 'is_like_count','is_view_count','isLiked','isViewed')
#
#     def get_isLiked(self, obj):
#         requestUser = self.context['request'].user
#         return PostLike.objects.filter(post=obj, user=requestUser).exists()
#
#     def get_isViewed(self, obj):
#         requestUser = self.context['request'].user
#         return PostView.objects.filter(post=obj, user=requestUser).exists()


class UserEditSerilaizer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'birth_date',
            'mobile',
            'bio',
            'about',
            'country_code',
            'gender',
            'passion',)


class UserMediaEditSerializer(ModelSerializer):

    # def get_isViewed(self, obj):
    #     requestUser = self.context['request'].user
    #     return MediaView.objects.filter(media=obj, user=requestUser).exists()

    class Meta:
        model = MediaPost
        fields = (
            'id',
            'user',
            'like_count',
            'view_count',
            'media',
            'share_count',
            'caption')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserEditSerilaizer(instance.user).data
        return response


class MediaPostSerializers(ModelSerializer):

    # def get_isViewed(self, obj):
    #     requestUser = self.context['request'].user
    #     return MediaView.objects.filter(media=obj, user=requestUser).exists()

    class Meta:
        model = MediaPost
        fields = ('id',

                  'like_count',
                  'view_count',
                  'media',
                  'user_media',
                  'share_count',
                  'caption')


class GetMediaPostSerializers(ModelSerializer):

    # def get_isViewed(self, obj):
    #     requestUser = self.context['request'].user
    #     return MediaView.objects.filter(media=obj, user=requestUser).exists()
    # is_friend_acc = serializers.SerializerMethodField()
    # is_user = serializers.SerializerMethodField()

    # def get_is_user(self, obj):
   
    #     user = self.context['request']
    #     if user == obj.user_id:
    #     # friend_data = FriendList.objects.filter(user=user, friends=obj.user_id)
    #         
    #     # if friend_data:
    #         return True
    #     else:
    #         return False
    # def get_is_friend_acc(self, obj):
   
    #     user = self.context['request']
    #     friend_data = FriendList.objects.filter(user=user, friends=obj.user_id)
    
    #     if friend_data:
    #         return True
    #     else:
    #         return False

    
    class Meta:
        model = MediaPost
        fields = ('user',
                  'like_count',
                  'media',
                  'id',
                  'caption',
                  'show_media_photo',
                #   'is_user',
                #   'is_friend_acc',
                'user_media',
                  )

class GetMediaPostV2Serializers(ModelSerializer):

    # def get_isViewed(self, obj):
    #     requestUser = self.context['request'].user
    #     return MediaView.objects.filter(media=obj, user=requestUser).exists()
    is_friend_acc = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()

    def get_is_user(self, obj):
       
        user = self.context['request1']
        if user == obj.user_id:
        # friend_data = FriendList.objects.filter(user=user, friends=obj.user_id)
           
        # if friend_data:
            return True
        else:
            return False
    def get_is_friend_acc(self, obj):
        
        user = self.context['request1']
        friend_data = FriendList.objects.filter(user=user, friends=obj.user_id)
       
        if friend_data:
            return True
        else:
            return False

    
    class Meta:
        model = MediaPost
        fields = ('user',
                  'like_count',
                  'media',
                  'user_media',
                  'id',
                  'caption',
                  'show_media_photo',
                  'is_user',
                  'is_friend_acc',
                  )




class GetMediaV2PostSerializers(ModelSerializer):
    isLiked = serializers.SerializerMethodField()
    # isViewed = serializers.SerializerMethodField()

    def get_isLiked(self, obj):
        requestUser = self.context['request'].user
        return MediaLike.objects.filter(media=obj, user=requestUser).exists()

    # def get_isViewed(self, obj):
    #     requestUser = self.context['request'].user
    #     return MediaView.objects.filter(media=obj, user=requestUser).exists()

    class Meta:
        model = MediaPost
        fields = ('id', 'user', 'isLiked', 'like_count', 'media', 'caption')


# class MediaViewSerializers(ModelSerializer):
#     class Meta:
#         model = MediaView
#         fields = "__all__"


class MediaLikeSerializers(ModelSerializer):
    class Meta:
        model = MediaLike
        fields = "__all__"


# class MediaShareSerializers(ModelSerializer):
#     class Meta:
#         model = MediaShare
#         fields = "__all__"


class GetUserVideoSerialize(ModelSerializer):

    is_friend_acc = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()

    def get_is_user(self, obj):
        
        user = self.context['request']
        if user == obj.user_id:
        # friend_data = FriendList.objects.filter(user=user, friends=obj.user_id)
            
        # if friend_data:
            return True
        else:
            return False
    def get_is_friend_acc(self, obj):
        
        user = self.context['request']
        friend_data = FriendList.objects.filter(user=user, friends=obj.user_id)
        
        if friend_data:
            return True
        else:
            return False
    class Meta:
        model = MediaVideo
        fields = ('user',
                  'like_count',
                  'media_video',
                  'id',
                  'video_caption',
                  'show_media_video',
                  'is_user',
                  'is_friend_acc',
                  )

class GetUserVideoSerialize(ModelSerializer):

    is_friend_acc = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()

    def get_is_user(self, obj):
        
        user = self.context['request']
        if user == obj.user_id:
        # friend_data = FriendList.objects.filter(user=user, friends=obj.user_id)
            
        # if friend_data:
            return True
        else:
            return False
    def get_is_friend_acc(self, obj):
       
        user = self.context['request']
        friend_data = FriendList.objects.filter(user=user, friends=obj.user_id)
       
        if friend_data:
            return True
        else:
            return False
    class Meta:
        model = MediaVideo
        fields = ('user',
                  'like_count',
                  'media_video',
                  'id',
                  'video_caption',
                  'show_media_video',
                  'is_user',
                  'is_friend_acc',
                  )




#
class MediaPostReportSerialize(ModelSerializer):
    class Meta:
        model = MediaPostReport
        fields = "__all__"
