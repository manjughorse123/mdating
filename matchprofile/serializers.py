from .models import *
from rest_framework import serializers

class PostUserUpdateSerializer(serializers.ModelSerializer):

        class Meta:
            model  = PostUserUpdate
            fields = '__all__'


class PostUserReactSerializer(serializers.ModelSerializer):

        def validate(self, attrs):
            # import pdb;pdb.set_trace()
            if PostUserUpdate.objects.filter(user = attrs['user']):
                raise serializers.ValidationError(
                    {"friend request was  already send"})

            return attrs

        class Meta:
            model  = PostUserReact
            fields = '__all__'

    

class UserPassionMatchSerializer(serializers.ModelSerializer):

        class Meta:
            model  = UserPassion
            fields = '__all__'