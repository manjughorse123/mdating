import imp
from rest_framework import serializers

from friend.models import *
from account.serializers import *
from usermedia.models import *
from usermedia.serializers import *


class UserFriendSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        age = User.calculate_age(obj.birth_date)

        return age

    class Meta:
        model = User
        fields = ('name',
                  'id',
                  'image',
                  'country',
                  'birth_date',
                  'address',
                  'city',
                  'age',)


class FriendRequestSerializer(serializers.ModelSerializer):

    # def validate(self, attrs):
    #
    #     if attrs['friend']:
    #         friend =attrs['friend']
    #         if FriendRequest.objects.filter(friend=friend):
    #             raise serializers.ValidationError(
    #                 {"friend request was  already send"})

    #     return attrs

    def create(self, validated_data):
        to_user = validated_data.get('user')
        from_user = validated_data.get('friend')
        friend_request, created = FriendRequest.objects.update_or_create(
            user=to_user, friend=from_user)

        return friend_request

    class Meta:
        model = FriendRequest
        fields = (
            'friend',
            'friendrequestsent',
            'id')


class GetFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['friend'] = UserFriendSerializer(instance.friend).data
        response['user'] = UserFriendSerializer(instance.user).data
        return response


class FriendListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendList
        fields = ('user',
                  'friends',
                  'is_accepted',
                  'id',
                  'show_friend',
                  )


class FriendListSerializer(serializers.ModelSerializer):

    # def validate(self, attrs):

    #     # to_user= validated_data.get('friends')
    #     if FriendList.objects.filter(friends = attrs['friends']):
    #         raise serializers.ValidationError(
    #             {"friend request was  already accept"})
    #
    #     return attrs
    is_mutual = serializers.SerializerMethodField()

    def get_is_mutual(self, obj):
        requestUser = self.context['request'].user
        friend1 = FriendList.objects.filter(user_id=requestUser)
        friend2 = FriendList.objects.filter(user_id=str(obj['friends'].id))

        friend1_id_list = []
        friend2_id_list = []

        for i in range(len(friend1)):
            friend_id_data = friend1[i].friends
            friend1_id_list.append(friend_id_data)

        for i in range(len(friend2)):
            friend_id_data = friend2[i].friends
            friend2_id_list.append(friend_id_data)

        abs = [x for x in friend1_id_list if x in friend2_id_list]
        if not abs:
            return 0
        return len(abs)

    def create(self, validated_data):

        to_user = validated_data.get('friends')
        from_user = validated_data.get('user')
        friend_request, created = FriendList.objects.update_or_create(
            friends=to_user, user=from_user)

        return friend_request

    class Meta:
        model = FriendList
        fields = (
            'friends',
            'is_accepted',
            'is_mutual',
            'id',)


class FollowSerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        if FriendRequest.objects.filter(is_active=True):
            raise serializers.ValidationError(
                {"friend request was  already send"})

        return attrs

    def create(self, validated_data):

        to_user = validated_data.get('user')
        from_user = validated_data.get('friend')
        friend_request, created = FriendList.objects.update_or_create(
            user=to_user, friends=from_user)

        return friend_request

    class Meta:
        model = FriendRequest
        fields = "__all__"


# class SendFollowRequestSerializers(serializers.ModelSerializer):

#         # def validate(self, attrs):

#         #     if FollowRequest.objects.filter(follow=attrs['follow']):
#         #         raise serializers.ValidationError(
#         #             {" user is already follow"})

#         #     return attrs

#         def create(self, validated_data):

#             user= validated_data.get('user')
#             follow = validated_data.get('follow')
#             follow_request, created = FollowRequest.objects.update_or_create(
#             user =user , follow=follow)

#             return follow_request

#         class Meta:
#             model = FollowRequest
#             fields = '__all__'


class FollowRequestSerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        if FollowRequest.objects.filter(follow=attrs['follow']):
            raise serializers.ValidationError(
                {" user is already follow"})

        return attrs

    # def create(self, validated_data):
    #     user= validated_data.get('user')
    #     follow = validated_data.get('follow')
    #     follow_request, created = FollowRequest.objects.update_or_create(
    #     user =user , follow=follow)

    #     return follow_request

    class Meta:
        model = FollowRequest
        fields = (
            'follow',
            'id',)


class FollowAcceptSerializer(serializers.ModelSerializer):

    # def validate(self, attrs):

    # if FollowAccept.objects.filter(follow=attrs['follow']):
    #     raise serializers.ValidationError(
    #         {" Follower already Added"})
    #
    # return attrs

    def create(self, validated_data):

        user = validated_data.get('user')
        follow = validated_data.get('follow')
        follow_accept, created = FollowAccept.objects.update_or_create(
            user=user, follow=follow)

        return follow_accept

    class Meta:
        model = FollowAccept
        fields = "__all__"

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['follow'] = UserFriendSerializer(instance.follow).data
    #     return response


class FollowRequestFollowingSerializer(serializers.ModelSerializer):

    is_mutual = serializers.SerializerMethodField()

    def get_is_mutual(self, obj):
        # print(self)

        follow1 = FollowRequest.objects.filter(
            user_id=obj.user)
        follow2 = FollowRequest.objects.filter(
            user_id=obj.follow)

        follow1_id_list = []
        follow2_id_list = []

        for i in range(len(follow1)):
            friend_id_data = follow1[i].follow
            follow1_id_list.append(friend_id_data)

        for i in range(len(follow2)):
            friend_id_data = follow2[i].user
            follow2_id_list.append(friend_id_data)

        abs = [x for x in follow1_id_list if x in follow2_id_list]
        if not abs:
            return 0
        return len(abs)

    class Meta:
        model = FollowRequest
        fields = (
            'follow',
            'user',
            'is_follow',
            'id',
            'is_mutual',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['follow'] = UserFriendSerializer(instance.follow).data
        return response


class FollowRequestFollowerV2Serializer(serializers.ModelSerializer):

    is_mutual = serializers.SerializerMethodField()

    def get_is_mutual(self, obj):
        # print(self)

        follow1 = FollowRequest.objects.filter(
            user_id=obj.user)
        follow2 = FollowRequest.objects.filter(
            user_id=obj.follow)

        follow1_id_list = []
        follow2_id_list = []

        for i in range(len(follow1)):
            friend_id_data = follow1[i].follow
            follow1_id_list.append(friend_id_data)

        for i in range(len(follow2)):
            friend_id_data = follow2[i].user
            follow2_id_list.append(friend_id_data)

        abs = [x for x in follow1_id_list if x in follow2_id_list]
        if not abs:
            return 0
        return len(abs)

    class Meta:
        model = FollowRequest
        fields = (
            'user',
            'follow',
            'is_follow',
            'id',
            'is_mutual',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserFriendSerializer(instance.user).data
        return response


# FriendRequest list
class FriendRequestListSerializer(serializers.ModelSerializer):

    is_mutual = serializers.SerializerMethodField()

    def get_is_mutual(self, obj):
        friend1 = FriendList.objects.filter(user_id=obj.friend)
        friend2 = FriendList.objects.filter(user_id=obj.user)

        friend1_id_list = []
        friend2_id_list = []

        for i in range(len(friend1)):
            friend_id_data = friend1[i].friends
            friend1_id_list.append(friend_id_data)

        for i in range(len(friend2)):
            friend_id_data = friend2[i].friends
            friend2_id_list.append(friend_id_data)

        abs = [x for x in friend1_id_list if x in friend2_id_list]
        if not abs:
            return 0
        return len(abs)

    class Meta:
        model = FriendRequest
        fields = (
            'friend',
            'user',
            'is_mutual',
            'id',)

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['friend'] = UserFriendSerializer(instance.friend).data
    #     return response

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserFriendSerializer(instance.user).data
        return response

# SendRequestListSerializer


class SendRequestListSerializer(serializers.ModelSerializer):

    is_mutual = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()

    def get_media(self, obj):

        medias_data = MediaPost.objects.filter(user=obj.friend)
        media_data = GetMediaPostSerializers(medias_data, many=True)

        return media_data.data

    def get_is_mutual(self, obj):
        friend1 = FriendList.objects.filter(user_id=obj.friend)
        friend2 = FriendList.objects.filter(user_id=obj.user)

        friend1_id_list = []
        friend2_id_list = []

        for i in range(len(friend1)):
            friend_id_data = friend1[i].friends
            friend1_id_list.append(friend_id_data)

        for i in range(len(friend2)):
            friend_id_data = friend2[i].friends
            friend2_id_list.append(friend_id_data)

        abs = [x for x in friend1_id_list if x in friend2_id_list]
        return len(abs)

    class Meta:
        model = FriendRequest
        fields = (
            'friend',
            'user',
            'is_mutual',
            'media',
            'id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['friend'] = UserFriendSerializer(instance.friend).data
        return response

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['user'] = UserFriendSerializer(instance.user).data
    #     return response


# FriendRequest  Accept list

class FriendRequestAcceptSerializer(serializers.ModelSerializer):
    is_mutual = serializers.SerializerMethodField()

    def get_is_mutual(self, obj):
        friend1 = FriendList.objects.filter(user_id=obj.friends)
        friend2 = FriendList.objects.filter(user_id=obj.user)

        friend1_id_list = []
        friend2_id_list = []

        for i in range(len(friend1)):
            friend_id_data = friend1[i].friends
            friend1_id_list.append(friend_id_data)

        for i in range(len(friend2)):
            friend_id_data = friend2[i].friends
            friend2_id_list.append(friend_id_data)

        abs = [x for x in friend1_id_list if x in friend2_id_list]

        if not abs:
            return 0
        return len(abs)

    class Meta:
        model = FriendList
        fields = ('friends', 'id', 'user', 'is_mutual', 'show_friend',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['friends'] = UserFriendSerializer(instance.friends).data
        return response


class FollowListFollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowAccept
        fields = ('follow', 'id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['follow'] = UserFriendSerializer(instance.follow).data
        return response


class SendFollowRequestSerializer(serializers.ModelSerializer):

    # def validate(self, attrs):
    #     if attrs['follow']:
    #         follow =attrs['follow']
    #         if FollowRequest.objects.filter(follow= follow):
    #             raise serializers.ValidationError(
    #                 {" user is alrady follow"})
    #         return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        follow = validated_data.get('follow')
        follow_request, created = FollowRequest.objects.update_or_create(
            user=user, follow=follow)

        return follow_request

    class Meta:
        model = FollowRequest
        fields = ('follow', 'is_follow', 'id',)

    #    FollowBackSerializer


class FollowBackSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = validated_data.get('user')
        follow = validated_data.get('follow')
        follow_request, created = FollowRequest.objects.update_or_create(
            user=user, follow=follow)

        return follow_request

    class Meta:
        model = FollowRequest
        fields = ('follow', 'is_follow', 'id',)


# class FollowBackSerializer(serializers.ModelSerializer):

#     def create(self, validated_data):
#         user = validated_data.get('user')
#         follow = validated_data.get('follow')
#         follow_request, created = FollowAccept.objects.update_or_create(
#             user=user, follow=follow)

#         return follow_request

#     class Meta:
#         model = FollowAccept
#         fields = ('follow', 'is_follow_accepted',)


class GetFollowBackSerializer(serializers.ModelSerializer):

    is_mutual = serializers.SerializerMethodField()

    def get_is_mutual(self, obj):
        # print(self)

        follow1 = FollowRequest.objects.filter(
            user_id=obj.user)
        follow2 = FollowRequest.objects.filter(
            user_id=obj.follow)

        follow1_id_list = []
        follow2_id_list = []

        for i in range(len(follow1)):
            friend_id_data = follow1[i].follow
            follow1_id_list.append(friend_id_data)

        for i in range(len(follow2)):
            friend_id_data = follow2[i].user
            follow2_id_list.append(friend_id_data)

        abs = [x for x in follow1_id_list if x in follow2_id_list]
        if not abs:
            return 0
        return len(abs)

    class Meta:
        model = FollowRequest
        fields = ('id', 'is_follow', 'user', 'follow', 'is_mutual')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['follow'] = UserFriendSerializer(instance.follow).data
        return response

# class GetFollowBackSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = FollowAccept
#         fields = '__all__'


class UserSuggestionSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    is_mutual = serializers.SerializerMethodField()

    def get_age(self, obj):
        # age = User.calculate_age(obj.birth_date)
        return obj.age

    def get_is_mutual(self, obj):

        requestuser = self.context['request']
        friend1 = FriendList.objects.filter(user_id=requestuser)
        friend2 = FriendList.objects.filter(user_id=obj)
        friend1_id_list = []
        friend2_id_list = []

        for i in range(len(friend1)):
            friend_id_data = friend1[i].friends
            friend1_id_list.append(friend_id_data)

        for i in range(len(friend2)):
            friend_id_data = friend2[i].friends
            friend2_id_list.append(friend_id_data)

        abs = [x for x in friend1_id_list if x in friend2_id_list]
        if not abs:
            return 0
        return len(abs)

    class Meta:
        model = User
        fields = ('name',
                  'id',
                  'image',
                  'country',
                  'birth_date',
                  'address',
                  'city',
                  'age',
                  'is_mutual',
                  'show_profile')
