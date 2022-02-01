from operator import add
from django.conf import settings
from rest_framework.generics import *
from .serializers import *
import random
import http.client

from rest_framework.generics import *
from rest_framework.views import *
from post.serializers import *
from usermedia.serializers import *
from .models import *
from .serializers import *
from friend.models import *
from friend.serializers import *


def send_otp(mobile, otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    headers = {'content-type': "application/json"}
    url = "http://control.msg91.com/api/sendotp.php?otp=" + otp + "&message=" + "Your otp is " + otp + "&mobile=" + mobile + "&authkey=" + authkey + "&country=91"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None


class Login(APIView):
    def post(self, request, *args, **kwargs):

        try:
            mobile = request.POST.get('mobile')
            country_code = request.POST.get('country_code')
            # otp = request.POST.get("otp")
            user = User.objects.filter(mobile=mobile, country_code=country_code).first()
            if user is None:
                return Response(
                    {"message": "mobile no. not registered", "success": False, 'is_register': False},
                    status=status.HTTP_404_NOT_FOUND)
            # otp = str(random.randint(999, 9999))
            otp = 1234
            user.otp = otp
            user.save()
            return Response({"message": "Done", "success": True, 'is_register': True, "user": {
                'id': user.id,
                'email': user.email,
                'mobile': user.mobile,
                'country_code': user.country_code,
                'name': user.name,
                # 'bio': user.bio,
                # 'birth_date': user.birth_date,
                # 'otp': user.otp,
                # 'relationship_status': user.relationship_status,
                # 'education': user.education,
                # 'body_type': user.body_type,
                # 'gender': user.gender,
                # # 'image':user_obj.image,
                # # 'userIntrest':user_obj.userinterest,
                # # 'idealmatch':user_obj.idealmatch,
                # 'height': user.height,
                # 'location': user.location,
                # # 'citylat': user.citylat,
                # # 'citylong': user.citylong,
                # 'address': user.address,
                # 'city': user.city,
                # 'is_premium': user.is_premium,
                'is_verified': user.is_verified}},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'success': False, 'message': 'internal server error'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Registration(APIView):
    def post(self, request):
        try:
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            country_code = request.POST.get('country_code')
            name = request.POST.get('name')
            birth_date = request.POST.get('birth_date')
            check_mobile = User.objects.filter(mobile=mobile).first()
            check_email = User.objects.filter(email=email).first()

            if check_mobile:
                return Response(
                    {"message": "mobile Already Exists", 'success': False, 'is_register': False, "mobile": mobile},
                    status=status.HTTP_400_BAD_REQUEST)
            if check_email:
                return Response(
                    {"message": "email Already Exists", 'success': False, 'is_register': False, "email": email},
                    status=status.HTTP_400_BAD_REQUEST)

            # otp = str(random.randint(999, 9999))
            otp = str(1234)
            user = User(email=email, name=name, birth_date=birth_date, mobile=mobile, otp=otp,
                        country_code=country_code)
            print(type(user))
            user.save()
            return Response({"message": "Your Registrations is successfully", "success": True, 'is_register': True,
                             "user": {
                                 'id': user.id,
                                 'email': user.email,
                                 'mobile': user.mobile,
                                 'country_code': user.country_code,
                                 'name': user.name,
                                 # 'bio': user.bio,
                                 # 'birth_date': user.birth_date,
                                 # 'otp': user.otp,
                                 # 'relationship_status': user.relationship_status,
                                 # 'education': user.education,
                                 # 'body_type': user.body_type,
                                 # 'gender': user.gender,
                                 # # 'image':user_obj.image,
                                 # # 'userIntrest':user_obj.userinterest,
                                 # # 'idealmatch':user_obj.idealmatch,
                                 # 'height': user.height,
                                 # 'location': user.location,
                                 # 'citylat': user.citylat,
                                 # 'citylong': user.citylong,
                                 # 'address': user.address,
                                 # 'city': user.city,
                                 # 'is_premium': user.is_premium,
                                 'is_verified': user.is_verified}},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'success': False, 'message': 'internal server error', 'is_register': False},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCreateView(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():

            # print (serializer.validated_data)
            # send_otp()
            email = serializer.validated_data['email']
            mobile = serializer.validated_data['mobile']
            msg = "New User Register"
            check_email = User.objects.filter(email=email).first()
            check_mobile = User.objects.filter(mobile=mobile).first()
            if check_email:
                return Response({"message": "User Already Exists with  This Email! "},
                                status=status.HTTP_400_BAD_REQUEST)
            if check_mobile:
                return Response({"message": "User Already Exists with This Phone NO!"},
                                status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            data = serializer.data
            if user:
                return Response({'data': data,
                                 "status": status.HTTP_201_CREATED,
                                 "msg": msg})
            else:
                return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OTPVerify(APIView):
    def post(self, request):
        try:
            mobile = request.POST.get("mobile")
            otp = request.POST.get("otp")
            country_code = request.POST.get("country_code")
            user_obj = User.objects.get(mobile=mobile, otp=otp, country_code=country_code)
            if user_obj.otp == otp:
                user_obj.is_phone_verified = True

                user_obj.save()
                return Response(
                    {'success': True, 'message': 'your OTP is verified', 'is_register': True, "user": {
                        'id': user_obj.id,
                        'email': user_obj.email,
                        'mobile': user_obj.mobile,
                        'country_code': user_obj.country_code,
                        'name': user_obj.name,
                        # 'bio': user_obj.bio,
                        # 'birth_date': user_obj.birth_date,
                        # 'otp': user_obj.otp,
                        # 'relationship_status': user_obj.relationship_status,
                        # 'education': user_obj.education,
                        # 'body_type': user_obj.body_type,
                        # 'gender': user_obj.gender,
                        # # 'image':user_obj.image,
                        # # 'userIntrest':user_obj.userinterest,
                        # # 'idealmatch':user_obj.idealmatch,
                        # 'height': user_obj.height,
                        # 'location': user_obj.location,
                        # 'citylat': user_obj.citylat,
                        # 'citylong': user_obj.citylong,
                        # 'address': user_obj.address,
                        # 'city': user_obj.city,
                        # 'is_premium': user_obj.is_premium,
                        'is_verified': user_obj.is_verified, }

                     },
                    status=status.HTTP_200_OK)
            return Response({'success': "success", 'message': 'Wrong OTP', "data": serializers.data},
                        status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            print(e)
        return Response({'success': False, 'message': 'internal server error ! or Mobile No. Not Registered', 'is_register': False},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserData(APIView):
    # def get(self, request, id, *args, **kwargs):
    #     user = User.objects.filter(id=id)
    #     post = PostUpload.objects.filter(user_id=id)
    #     media = UserMedia.objects.filter(user_id=id)
    #     userserializer = UserSerializer(user, many=True)
    #     postsrializer = PostUploadSerializers(post, many=True)
    #     mediaserializer = UserMediaSerializer(media, many=True)
    #     return Response({"message": True, "user": userserializer.data, "post":postsrializer.data, "media":mediaserializer.data}, status=status.HTTP_200_OK)

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        user = self.get_object(id)
        post = PostUpload.objects.filter(user_id=id)
        media = MediaPost.objects.filter(user_id=id)
        follow = FollowRequest.objects.filter(user_id=id)
        followaccept = FollowAccept.objects.filter(user_id=id)

        userserializer = UserSerializer(user)
        postsrializer = PostUploadSerializers(post, many=True)
        followserializer = FollowRequestSerializer(follow, many=True)
        followacceptserializer = FollowAcceptSerializer(followaccept, many=True)
        mediaserializer = MediaPostSerializers(media, many=True)
        return Response({"message": True, "user": userserializer.data, "PostCount": len(postsrializer.data),
                         "post": postsrializer.data, "MediaCount": len(mediaserializer.data),
                         "media": mediaserializer.data, "Following   ": len(followserializer.data),
                         "Follower": len(followacceptserializer.data),
                         }, status=status.HTTP_200_OK)




# "follow": followserializer.data,
# "followaccept": followacceptserializer.data}


class UserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddPassionView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        passion = Passion.objects.all()
        serializer = PassionSerializer(passion, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):

        serializer = PassionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddPassiondetailView(APIView):
    """
    Retrieve, update or delete  a Passion instance.
    """

    def get_object(self, pk):
        try:
            return Passion.objects.get(pk=pk)
        except Passion.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        addPassion = self.get_object(pk)
        serializer = PassionSerializer(addPassion)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        addPassion = self.get_object(pk)
        serializer = PassionSerializer(addPassion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):

        addPassion = self.get_object(pk)
        serializer = PassionSerializer(
            addPassion, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        addPassion = self.get_object(pk)
        addPassion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddGenderView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        gender = Gender.objects.all()
        serializer = GenderSerializer(gender, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):

        serializer = GenderSerializer(data=request.data)

        if serializer.is_valid():
            gender = serializer.validated_data['gender']
            check_gender = Gender.objects.filter(gender=gender).first()

            if check_gender:
                return Response({"message": "gender Already Exists with  This name! "},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddGenderdetailView(APIView):
    """
    Retrieve, update or delete  a Gender instance.
    """

    def get_object(self, pk):
        try:
            return Gender.objects.get(pk=pk)
        except Gender.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        addGender = self.get_object(pk)
        serializer = GenderSerializer(addGender)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        addGender = self.get_object(pk)
        serializer = GenderSerializer(addGender, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        addGender = self.get_object(pk)
        serializer = GenderSerializer(addGender, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        addGender = self.get_object(pk)
        addGender.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddUserMediaView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userMedia = UserMedia.objects.all()
        serializer = UserMediaSerializer(userMedia, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):

        serializer = UserMediaSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            check_name = UserMedia.objects.filter(name=name).first()

            if check_name:
                return Response({"message": "media Already Exists with  This name! "},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddUserMediadetailView(APIView):
    """
    Retrieve, update or delete  a media instance.
    """

    def get_object(self, pk):
        try:
            return UserMedia.objects.get(pk=pk)
        except UserMedia.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        addUserMedia = self.get_object(pk)
        serializer = UserMediaSerializer(addUserMedia)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        addUserMedia = self.get_object(pk)
        # addUserMedia['image'] =  
        addUserMedia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddMaritalStatusView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        meritalstatus = MaritalStatus.objects.all()
        serializer = MaritalStatusSerializer(meritalstatus, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):

        serializer = MaritalStatusSerializer(data=request.data)

        if serializer.is_valid():
            m_status = serializer.validated_data['status']
            check_status = MaritalStatus.objects.filter(status=m_status).first()

            if check_status:
                return Response({"message": "media Already Exists with  This name! "},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddMaritalStatusdetailView(APIView):
    """
    Retrieve, update or delete  a MaritalStatus instance.
    """

    def get_object(self, pk):
        try:
            return MaritalStatus.objects.get(pk=pk)
        except MaritalStatus.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        merital_status = self.get_object(pk)
        serializer = MaritalStatusSerializer(merital_status)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        merital_status = self.get_object(pk)
        serializer = MaritalStatusSerializer(merital_status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        merital_status = self.get_object(pk)
        serializer = MaritalStatusSerializer(merital_status, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        merital_status = self.get_object(pk)
        merital_status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddIdealMatchView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):

        idealMatch = IdealMatch.objects.all()

        serializer = IdealMatchSerializer(idealMatch, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = IdealMatchSerializer(data=request.data)

        if serializer.is_valid():
            idealmatch = serializer.validated_data['idealmatch']

            check_name = IdealMatch.objects.filter(idealmatch=idealmatch).first()

            if check_name:
                return Response({"message": "idealmatch Already Exists with  This name! "},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddIdealMatchdetailView(APIView):
    """
    Retrieve, update or delete  a media instance.
    """

    def get_object(self, pk):
        try:
            return IdealMatch.objects.get(pk=pk)
        except IdealMatch.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        addIdealMatch = self.get_object(pk)
        serializer = IdealMatchSerializer(addIdealMatch)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        addIdealMatch = self.get_object(pk)
        serializer = IdealMatchSerializer(addIdealMatch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        addIdealMatch = self.get_object(pk)
        serializer = IdealMatchSerializer(addIdealMatch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        addIdealMatch = self.get_object(pk)
        addIdealMatch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddUserImageView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        idealMatch = User.objects.all()
        serializer = UserImageSerializer(idealMatch, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):

        serializer = UserImageSerializer(data=request.data)

        if serializer.is_valid():
            # idealmatch = serializer.validated_data['idealmatch']
            # check_name =UserIdealMatch.objects.filter(idealmatch=idealmatch).first()

            # if check_name:
            #     return Response({"message": "idealmatch Already Exists with  This name! "}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# API FOR USER IDEAL  MATCH
class AddUserIdealMatchView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        useridealMatch = UserIdealMatch.objects.all()
        serializer = UserIdealMatchSerializer(useridealMatch, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserIdealMatchSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddUserIdealMatchdetailView(APIView):
    """
    Retrieve, update or delete  a media instance.
    """

    def get_object(self, pk):
        try:
            return UserIdealMatch.objects.get(pk=pk)
        except UserIdealMatch.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        adduserIdealMatch = self.get_object(pk)
        serializer = UserIdealMatchSerializer(adduserIdealMatch)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        adduserIdealMatch = self.get_object(pk)
        serializer = UserIdealMatchSerializer(adduserIdealMatch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        adduserIdealMatch = self.get_object(pk)
        serializer = UserIdealMatchSerializer(adduserIdealMatch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        adduserIdealMatch = self.get_object(pk)
        adduserIdealMatch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# API FOR USER INTERSET API
class AddUserPassionView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userPassion = UserPassion.objects.all()
        serializer = UserPassionSerializer(userPassion, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserPassionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddUserPassiondetailView(APIView):
    """
    Retrieve, update or delete  a media instance.
    """

    def get_object(self, pk):
        try:
            return UserPassion.objects.get(pk=pk)
        except UserPassion.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        adduserPassion = self.get_object(pk)
        serializer = UserPassionSerializer(adduserPassion)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        adduserPassion = self.get_object(pk)
        serializer = UserPassionSerializer(adduserPassion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        adduserPassion = self.get_object(pk)
        serializer = UserPassionSerializer(adduserPassion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        adduserPassion = self.get_object(pk)
        adduserPassion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
# <<<<<<< HEAD
# #             serializer.save()
# #             return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
# #         else:
# #             return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
# =======
#
#
#
# >>>>>>> b5e5b2d31123a3f0cda62178ca3edc335ec0c3d2

# class MatchProfileView(APIView):
#     # permission_classes = (AllowAny,)

#     def get(self, request):
#         lsit1 = []

#         if UserPassion.objects.filter(passion="[Art]"):
#             user_ideal =  UserPassion.objects.filter(passion=3)
#             lsit1.append(user_ideal)


#         if UserPassion.objects.filter(passion=5):
#             user_ideal1 =  UserPassion.objects.filter(passion=5)
#             lsit1.append(user_ideal1)

#         if UserIdealMatch.objects.filter(idealmatch=2):
#             user_ideal =  UserIdealMatch.objects.filter(idealmatch=2)
#             lsit1.append(user_ideal)

#         return Response({"success": "True" , "data" : lsit1}, status=status.HTTP_200_OK)

# from django.db.models import Q
# class MatchProfileView(ModelViewSet):
#     queryset = UserPassion.objects.order_by("-passion")
#     serializer_class = UserPassionSerializer
#     # filterset_class = UserPassionMatchFilter

#     def get_queryset(self):
#         import pdb;pdb.set_trace()
#         queryset = self.queryset

#         q_name = Q()
#         rel_name = self.request.query_params.get("[Technology]", None)
#         if rel_name:
#             q_name = Q(users__name=rel_name)

#         # q_groups = Q()
#         # rel_groups = self.request.query_params.get("Techlogy", "").split(",")
#         # if any(rel_groups):
#         #     q_groups = Q(groups__name__in=rel_groups)

#         qs = queryset.filter(q_name).distinct()
#         return qs

class MatchProfileView(APIView):

    def get(self, request):

        if UserPassion.objects.filter(passion=1):
            userPassion = UserPassion.objects.filter(passion=1)
            serializer = UserPassionSerializer(userPassion, many=True)

        if UserPassion.objects.filter(passion=2):
            userPassion = UserPassion.objects.filter(passion=2)
            serializer = UserPassionSerializer(userPassion, many=True)

        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)
