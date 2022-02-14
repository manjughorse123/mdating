from .models import *
from rest_framework import serializers


class FriendRequestSerializer(serializers.ModelSerializer):
   
        def validate(self, attrs):
            # import pdb;pdb.set_trace()
            if attrs['receiver']:
                receiver =attrs['receiver']
                if FriendRequest.objects.filter(receiver=receiver):
                    raise serializers.ValidationError(
                        {"friend request was  already send"})

            return attrs

        def create(self, validated_data):
            # import pdb;pdb.set_trace()
            to_user= validated_data.get('receiver')
            from_user = validated_data.get('sender')
            friend_request, created = FriendRequest.objects.update_or_create(
             receiver=to_user , sender=from_user)
            
            return friend_request

        class Meta:
            model = FriendRequest
            fields = '__all__'



# def validate(self, attrs):
#         if attrs['password'] != attrs['confrim_password']:

#             raise serializers.ValidationError(
#                 {"password": "Password fields didn't match."})

#         if int(attrs['mobile']) < 10:

#             raise serializers.ValidationError(
#                 {"Mobile no": "no  should be  10 digit."})

#         return attrs


class FriendListSerializer(serializers.ModelSerializer):
   
        def validate(self, attrs):
            # import pdb;pdb.set_trace()
            # to_user= validated_data.get('friends')
            if FriendList.objects.filter(friends = attrs['friends']):
                raise serializers.ValidationError(
                    {"friend request was  already accept"})

            return attrs
    
        def create(self, validated_data):
            # import pdb;pdb.set_trace()
            to_user= validated_data.get('friends')
            from_user = validated_data.get('user')
            friend_request, created = FriendList.objects.update_or_create(
            friends =to_user , user=from_user)
            
            return friend_request

        class Meta:
            model = FriendList
            fields = "__all__"



class FollowSerializer(serializers.ModelSerializer):
   
        def validate(self, attrs):
            # import pdb;pdb.set_trace()
            if FriendRequest.objects.filter(is_active = True):
                raise serializers.ValidationError(
                    {"friend request was  already send"})

            return attrs

        def create(self, validated_data):
            # import pdb;pdb.set_trace()
            to_user= validated_data.get('receiver')
            from_user = validated_data.get('sender')
            friend_request, created = FriendList.objects.update_or_create(
            user =to_user , friends=from_user)
            
            return friend_request

        class Meta:
            model = FriendRequest
            fields = "__all__"



class FollowRequestSerializer(serializers.ModelSerializer):
   
        def validate(self, attrs):
            # import pdb;pdb.set_trace()
            # follow = validate.get()
            if FollowRequest.objects.filter(follow= attrs['follow']):
                raise serializers.ValidationError(
                    {" user is alrady follow"})

            return attrs

        def create(self, validated_data):
            # import pdb;pdb.set_trace()
            user= validated_data.get('user')
            follow = validated_data.get('follow')
            follow_request, created = FollowRequest.objects.update_or_create(
            user =user , follow=follow)
            
            return follow_request

        class Meta:
            model = FollowRequest
            fields = "__all__"

    

class FollowAcceptSerializer(serializers.ModelSerializer):
   
        def validate(self, attrs):
            # import pdb;pdb.set_trace()
            if FollowAccept.objects.filter(follow=attrs['follow']):
                raise serializers.ValidationError(
                    {" Follower already Added"})

            return attrs

        def create(self, validated_data):
            # import pdb;pdb.set_trace()
            user= validated_data.get('user')
            follow = validated_data.get('follow')
            follow_accept, created = FollowAccept.objects.update_or_create(
            user =user , follow=follow)
            
            return follow_accept

        class Meta:
            model = FollowAccept
            fields = "__all__"

class FAQSerializer(serializers.ModelSerializer):

        class Meta:
            model  = FAQ
            fields = "__all__"


class FollowRequestFollowerSerializer(serializers.ModelSerializer):

        class Meta:
            model  = FollowRequest
            fields = ('follow',)



# FriendRequest list
class FriendRequestListSerializer(serializers.ModelSerializer):

        class Meta:
            model  = FriendRequest
            fields = ('sender',)


class FollowListFollowingSerializer(serializers.ModelSerializer):

        class Meta:
            model  = FollowAccept
            fields = ('follow',)
