
from rest_framework import serializers

from account.models import *
from friend.models import *
from post.models import *
from usermedia.models import MediaPost, MediaVideo


class PassionSerializer(serializers.ModelSerializer):
    passion = serializers.CharField(max_length=100)

    class Meta:
        model = Passion
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
 
    class Meta(object):

        model = User
        fields = "__all__"
        

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['gender'] = GenderSerializer(instance.gender).data

        response['interest_in'] = GenderSerializer(instance.interest_in).data
        response['tall'] = HeightSerializer(instance.tall).data
        response['marital_status'] = MaritalStatusSerializer(
            instance.marital_status).data

        return response


class UserProfileSerializer(serializers.ModelSerializer):
    
    user_passion = serializers.SerializerMethodField()
    user_idealmatch = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    is_get_friend_request = serializers.SerializerMethodField()
    is_send_friend_request = serializers.SerializerMethodField()
    is_follower = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()
    pro_image = serializers.SerializerMethodField()

    def get_pro_image(self, obj):

        return True
    # profile_image = serializers.SerializerMethodField()

    # def get_profile_image(self, obj):
    #     request = self.context.get('request')
    #     return request.build_absolute_uri(obj.file.url)

    def get_is_user(self, obj):
       
        user = self.context['request1']
        user_data = User.objects.get(
            id=user)
        user_datas = User.objects.get(
            id=obj.id)
        if user_data == user_datas:
            return True
        else:
            return False

    def get_user_passion(self, obj):
        if (obj.passion.count()) > 0:
            splitlist1 = obj.passion.all()
            user_passion = PassionSerializer(splitlist1, many=True)
            # user_passion = ",".join([str(i.passion) for i in splitlist1])
            return user_passion.data
        else:
            return "-"

    def get_user_idealmatch(self, obj):
        if (obj.idealmatch.count()) > 0:
            splitlist1 = obj.idealmatch.all()
            user_idealmatch = IdealMatchSerializer(splitlist1, many=True)
            return user_idealmatch.data
        else:
            return "-"

    def get_is_friend(self, obj):
        user = self.context['request1']
        friend_data = FriendList.objects.filter(
            user=user, friends=obj.id)

        data = True if friend_data else False
        return data

    def get_is_get_friend_request(self, obj):
        user = self.context['request1']
        friend_data = FriendRequest.objects.filter(
            user=obj.id, friend=user)
        data = True if friend_data else False
        return data

    def get_is_send_friend_request(self, obj):
        user = self.context['request1']
        friend_data = FriendRequest.objects.filter(
            user=user, friend=obj.id)

        data = True if friend_data else False
        return data

    def get_is_following(self, obj):
        user = self.context['request1']
        follower_info = FollowRequest.objects.filter(
            follow_id=user, user_id=obj.id)

        data = True if follower_info else False
        return data

    def get_is_follower(self, obj):
        user = self.context['request1']
        follower_info = FollowRequest.objects.filter(
            follow_id=obj.id, user_id=user)

        data = True if follower_info else False
        return data

    class Meta:

        model = User
        fields = ('name',
            'profile_image',
                  'id',
                  'gender',
                  'passion',
                  'country_code',
                  'mobile',
                  'birth_date',
                  'image',
                  'bio',
                  'about',
                  'interest_in',
                  'tall',
                  'marital_status',
                  'idealmatch',
                  'email',
                  'user_passion',
                  'user_idealmatch',
                  'city',
                  'location',
                  'show_profile',
                  "is_friend",
                  'is_get_friend_request',
                  'is_send_friend_request',
                  "is_follower",
                  'is_following',
                  'is_user',
                  
                  'user_verified_status',
                #   'profile_image',
                'pro_image',
                )
        


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['gender'] = GenderSerializer(instance.gender).data

        response['interest_in'] = GenderSerializer(instance.interest_in).data
        response['tall'] = HeightSerializer(instance.tall).data
        response['marital_status'] = MaritalStatusSerializer(
            instance.marital_status).data

        return response


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for Regiter User endpoint.
    """
    email = serializers.EmailField(
        required=True,
    )

    def validate(self, attrs):

        if int(attrs['mobile']) < 10:
            raise serializers.ValidationError(
                {"Mobile no": "no  should be  10 digit."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email']
        )

        # user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


class GenderSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(max_length=200)
    icon = serializers.ImageField(
        max_length=None, use_url=True,
    )
    icon = serializers.CharField(max_length=100)

    class Meta:
        model = Gender
        fields = "__all__"


class IdealMatchSerializer(serializers.ModelSerializer):
    idealmatch = serializers.CharField(max_length=200)
    icon = serializers.ImageField(
        max_length=None, use_url=True,
    )
    icon = serializers.CharField(max_length=100)

    class Meta:
        model = IdealMatch
        fields = "__all__"


class MaritalStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=200)
    icon = serializers.ImageField(
        max_length=None, use_url=True,
    )
    icon = serializers.CharField(max_length=100)

    class Meta:
        model = MaritalStatus
        fields = "__all__"


class HeightSerializer(serializers.ModelSerializer):
    """
    Serializer for User Ideal Match
    """

    class Meta:
        model = Heigth
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for User Detail
    """

    class Meta:
        model = User
        fields = ('id', 'name', 'is_gender', 'is_passion', 'is_tall', 'is_location',
                  'is_interest_in', 'is_idealmatch', 'is_marital_status', 'is_media', 'is_complete_profile','user_verified_status','is_register_user_verified',)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login
    """

    class Meta:
        model = User
        fields = ('mobile', 'country_code', 'otp',)


class UserOtpSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login
    """

    class Meta:
        model = User
        fields = ('mobile', 'country_code')


class UserGenderSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login
    """

    class Meta:
        model = User
        fields = ('gender',)
        read_only_fields = ('id', 'email', 'name', 'mobile',)


class UserVerifiedSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'is_register_user_verified','user_verified_status','is_register_user_verified','active_reseaon',)


class UserVerifyDocSerializer(serializers.ModelSerializer):
    # govt_id_image = serializers.CharField(max_length=200)
    # selfie_image = serializers.CharField(max_length=200)

    class Meta:

        model = User
        fields = ('id', 'govt_id_url', 'selfie_url','user_verified_status','is_register_user_verified','active_reseaon',)


class UserResendOtpSerializer(serializers.ModelSerializer):
    # govt_id = serializers.CharField(max_length=200)
    # selfie = serializers.CharField(max_length=200)

    class Meta:

        model = User
        fields = ('id',
                  'mobile',
                  'country_code')


class UserSettingSerializer(serializers.ModelSerializer):

    show_friend = serializers.SerializerMethodField()
    show_public_post = serializers.SerializerMethodField()
    show_private_post = serializers.SerializerMethodField()
    show_media_photo = serializers.SerializerMethodField()
    show_media_video = serializers.SerializerMethodField()

    def get_show_friend(self, obj):

        friend_data = FriendList.objects.filter(user=obj.id)
        if len(friend_data) > 0:
            for i in range(len(friend_data)):
                data = friend_data[i].show_friend
            return data
        return 2

    def get_show_public_post(self, obj):
        public_data = PostUpload.objects.filter(user=obj.id, is_private=0)
        if len(public_data) > 0:
            for i in range(len(public_data)):
                data = public_data[i].show_public_post
            return data
        return 0

    def get_show_private_post(self, obj):
        public_data = PostUpload.objects.filter(user=obj.id, is_private=1)
       
        if len(public_data) > 0:
            for i in range(len(public_data)):
                data = public_data[i].show_private_post
               
            return data
        return 2

    def get_show_media_photo(self, obj):
        media_photo = MediaPost.objects.filter(user=obj.id)
        if len(media_photo) > 0:
            for i in range(len(media_photo)):
                data = media_photo[i].show_media_photo
            return data
        return 2

    def get_show_media_video(self, obj):
        media_video = MediaVideo.objects.filter(user=obj.id)
        print("hgsqjhgjah ------>",media_video)
        if len(media_video) > 0:
            for i in range(len(media_video)):
                data = media_video[i].show_media_video
            return data
        return 2

    class Meta(object):
        model = User
        fields = ('id',
                  'name',
                  'mobile',
                  'gender',
                  'passion',
                  'show_profile',
                  'show_friend',
                  'show_public_post',
                  'show_private_post',
                  'show_media_photo',
                  'show_media_video',)
