from account.models import *
from rest_framework import serializers
from .models import *

# class FriendListSerializer(serializers.ModelSerializer):

#         def validate(self, attrs):
#
#             # to_user= validated_data.get('friends')
#             if FriendList.objects.filter(friends = attrs['friends']):
#                 raise serializers.ValidationError(
#                     {"friend request was  already accept"})

#             return attrs

#         def create(self, validated_data):
#
#             to_user= validated_data.get('friends')
#             from_user = validated_data.get('user')
#             friend_request, created = FriendList.objects.update_or_create(
#             friends =to_user , user=from_user)

#             return friend_request

#         class Meta:
#             model = FriendList
#             fields = "__all__"


# class FollowSerializer(serializers.ModelSerializer):

#         def validate(self, attrs):
#
#             if FriendRequest.objects.filter(is_active = True):
#                 raise serializers.ValidationError(
#                     {"friend request was  already send"})

#             return attrs

#         def create(self, validated_data):
#
#             to_user= validated_data.get('user')
#             from_user = validated_data.get('friend')
#             friend_request, created = FriendList.objects.update_or_create(
#             user =to_user , friends=from_user)

#             return friend_request

#         class Meta:
#             model = FriendRequest
#             fields = "__all__"


# class FollowRequestSerializer(serializers.ModelSerializer):

#         def validate(self, attrs):
#
#             # follow = validate.get()
#             if FollowRequest.objects.filter(follow= attrs['follow']):
#                 raise serializers.ValidationError(
#                     {" user is alrady follow"})

#             return attrs

#         def create(self, validated_data):
#
#             user= validated_data.get('user')
#             follow = validated_data.get('follow')
#             follow_request, created = FollowRequest.objects.update_or_create(
#             user =user , follow=follow)

#             return follow_request

#         class Meta:
#             model = FollowRequest
#             fields = "__all__"


# class FollowAcceptSerializer(serializers.ModelSerializer):

#         def validate(self, attrs):
#
#             if FollowAccept.objects.filter(follow=attrs['follow']):
#                 raise serializers.ValidationError(
#                     {" Follower already Added"})

#             return attrs

#         def create(self, validated_data):
#
#             user= validated_data.get('user')
#             follow = validated_data.get('follow')
#             follow_accept, created = FollowAccept.objects.update_or_create(
#             user =user , follow=follow)

#             return follow_accept

#         class Meta:
#             model = FollowAccept
#             fields = "__all__"

# class UserLikeflagSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserLike
#         fields = '__all__'


# class UserLikeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserLike
#         fields = '__all__'


# class MatchesprofileSerializer(serializers.ModelSerializer):

#     """
#     Serializer for User UserPassion
#     """
#     class Meta:
#         model = Matchesprofile
#         fields = '__all__'
