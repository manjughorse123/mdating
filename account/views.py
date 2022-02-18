from operator import add
from django.conf import settings
from rest_framework import viewsets
from rest_framework.generics import *

import http.client
from rest_framework.generics import GenericAPIView
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


class Login(GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):

        try:
            mobile = request.POST.get('mobile')
            country_code = request.POST.get('country_code')
            # otp = request.POST.get("otp")
            user = User.objects.filter(mobile=mobile, country_code=country_code).first()
            if user is None:
                return Response(
                    {"message": "mobile no. not registered", "success": False, 'is_register': False,"status" : 404},
                    status=status.HTTP_404_NOT_FOUND)
            # otp = str(random.randint(999, 9999))
            otp = 1234
            user.otp = otp
            user.save()
            return Response({"message": "User Login Successfully!", "status": 200 ,"success": True, 'is_register': True, "user": {
                'id': user.id,
                'email': user.email,
                'mobile': user.mobile,
                'country_code': user.country_code,
                'name': user.name,
                'is_verified': user.is_verified}},
                            status=status.HTTP_200_OK)
            # else :
            #     return Response({'success': False, "status": 404, 'message': 'Field Required'},
            #                 status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            return Response({'success': False, "status" : 404 ,'message': 'internal server error'},
                            status=status.HTTP_404_NOT_FOUND)


class Registration(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):

        try:

            email = request.data['email']
            mobile = request.data['mobile']
            country_code = request.data['country_code']
            name = request.data['name']
            birth_date = request.data['birth_date']
            check_mobile = User.objects.filter(mobile=mobile).first()
            check_email = User.objects.filter(email=email).first()

            if check_mobile:
                return Response(
                    {"message": "Mobile Number Already Exists!", 'status' : 400,'success': False, 'is_register': False, "mobile": mobile},
                    status=status.HTTP_400_BAD_REQUEST)
            if check_email:
                return Response(
                    {"message": "email Already Exists", 'success': False, 'status' : 400,'is_register': False, "email": email},
                    status=status.HTTP_400_BAD_REQUEST)

            # otp = str(random.randint(999, 9999))
            otp = str(1234)
            user = User(email=email, name=name, birth_date=birth_date, mobile=mobile, otp=otp,
                        country_code=country_code)
            print(type(user))
            user.save()
            return Response({"message": "Your Registrations is successfully","status" : 201, "success": True, 'is_register': True,
                             "user": {
                                 'id': user.id,
                                 'email': user.email,
                                 'mobile': user.mobile,
                                 'country_code': user.country_code,
                                 'name': user.name,
                                 'is_verified': user.is_verified}},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'success': False,  'status' :400 ,  'message': 'User Not Register','is_register': False},
                            status=status.HTTP_400_BAD_REQUEST)


class UserCreateView(GenericAPIView):
    serializer_class =  RegisterSerializer
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
                                 "status": 201,
                                 "msg": msg},status =status.HTTP_201_CREATED)
            else:
                return Response({"data": serializer.errors,"status": 400 }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data": serializer.errors,"status": 400}, status=status.HTTP_400_BAD_REQUEST)


class OTPVerify(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        try:
            mobile = request.POST.get("mobile")
            otp = request.POST.get("otp")
            country_code = request.POST.get("country_code")
            user_obj = User.objects.get(mobile=mobile, otp=otp, country_code=country_code)
            if user_obj.otp == otp:
                user_obj.is_phone_verified = True

                user_obj.save()
                if (user_obj.gender_field and user_obj.passion_field and user_obj.height_field  and user_obj.location_field and
                    user_obj.interest_in_field and user_obj.idealmatch_field and user_obj.relationship_status_field  and user_obj.is_media_field) == True:
                    is_complete_profile = True
                else :
                    is_complete_profile = False

                return Response(
                    {'success': True, 'message': 'your OTP is verified', 'status': 200,'is_register': True, "user": {
                        'id': user_obj.id,
                        'email': user_obj.email,
                        'mobile': user_obj.mobile,
                        'country_code': user_obj.country_code,
                        'name': user_obj.name,
                        "is_complete_profile": is_complete_profile,
                        'is_verified': user_obj.is_verified, }

                     },
                    status=status.HTTP_200_OK)
            return Response({'success': "success", 'message': 'Wrong OTP', "status": 403,"data": serializers.data},
                            status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            print(e)
        return Response(
            {'success': False, 'message': ' Mobile Number Not Registered','status': 404, 'is_register': False},
            status=status.HTTP_404_NOT_FOUND)


class UserData(GenericAPIView):
    serializer_class = (UserSerializer )

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
        return Response({"message": True, "user": userserializer.data,"status": 200, "PostCount": len(postsrializer.data),
                         "post": postsrializer.data, "MediaCount": len(mediaserializer.data),
                         "media": mediaserializer.data, "Following   ": len(followserializer.data),
                         "Follower": len(followacceptserializer.data),
                         }, status=status.HTTP_200_OK)


class UserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        # object = User.objects.get(pk=pk)

        question = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(question, data=request.data, partial=True)

        if serializer.is_valid():
            question = serializer.save()

            return Response({"message" : "User Data is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AddPassionView(GenericAPIView):
    # permission_classes = (AllowAny,)
    serializer_class = PassionSerializer

    def get(self, request):
        passion = Passion.objects.all()
        serializer = PassionSerializer(passion, many=True)
        return Response({"success": True, "base_url": "http://18.224.254.170" , "status" : 200, "data": serializer.data}, status=status.HTTP_200_OK)

    # def post(self, request, format='json'):
    #     serializer = PassionSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"success": True, "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({"success": "error", "status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddGenderView(GenericAPIView):
    # permission_classes = (AllowAny,)
    serializer_class = GenderSerializer

    def get(self, request):
        gender = Gender.objects.all()
        serializer = GenderSerializer(gender, many=True)
        return Response({"success": True, "base_url": "http://18.224.254.170/media/" , "status" : 200,"data": serializer.data}, status=status.HTTP_200_OK)

    # def post(self, request, format='json'):
    #     serializer = GenderSerializer(data=request.data)
    #     if serializer.is_valid():
    #         gender = serializer.validated_data['gender']
    #         check_gender = Gender.objects.filter(gender=gender).first()
    #
    #         if check_gender:
    #             return Response({"message": "Gender Already Exists with  This name! "},
    #                             status=status.HTTP_400_BAD_REQUEST)
    #         serializer.save()
    #         return Response({"success": True,"base_url": "http://18.224.254.170/media/" , "status" : 201
    #                             , "data": serializer.data}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class AddUserMediaView(GenericAPIView):
    # permission_classes = (AllowAny,)
    serializer_class = UserMediaSerializer
    def get(self, request):
        userMedia = UserMedia.objects.all()
        serializer = UserMediaSerializer(userMedia, many=True)
        return Response({"success": True, "status" : 200, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):

        serializer = UserMediaSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
            check_name = UserMedia.objects.filter(name=name).first()

            if check_name:
                return Response({"message": "media Already Exists with  This name! "},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"success": True, "status" : 201,"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error","status" : 200,  "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddMaritalStatusView(GenericAPIView):
    serializer_class = MaritalStatusSerializer
    # permission_classes = (AllowAny,)

    def get(self, request):
        meritalstatus = MaritalStatus.objects.all()
        serializer = MaritalStatusSerializer(meritalstatus, many=True)
        return Response({"success": True, "status" : 200,"base_url": "http://18.224.254.170/media/","data": serializer.data}, status=status.HTTP_200_OK)

    # def post(self, request, format='json'):
    #
    #     serializer = MaritalStatusSerializer(data=request.data)
    #
    #     if serializer.is_valid():
    #         m_status = serializer.validated_data['status']
    #         check_status = MaritalStatus.objects.filter(status=m_status).first()
    #
    #         if check_status:
    #             return Response({"message": "media Already Exists with  This name! "},
    #                             status=status.HTTP_400_BAD_REQUEST)
    #         serializer.save()
    #         return Response({"success": True,  "status" : 201 ,"data": serializer.data}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({"success": "error", "status" : 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddIdealMatchView(GenericAPIView):
    serializer_class = IdealMatchSerializer
    # permission_classes = (AllowAny,)

    def get(self, request):

        idealMatch = IdealMatch.objects.all()

        serializer = IdealMatchSerializer(idealMatch, many=True)
        return Response({"success": True,"base_url": "http://18.224.254.170/media/", "status" : 200,"data": serializer.data}, status=status.HTTP_200_OK)

    # def post(self, request, format='json'):
    #     serializer = IdealMatchSerializer(data=request.data)
    #
    #     if serializer.is_valid():
    #         idealmatch = serializer.validated_data['idealmatch']
    #
    #         check_name = IdealMatch.objects.filter(idealmatch=idealmatch).first()
    #
    #         if check_name:
    #             return Response({"message": "idealmatch Already Exists with  This name! "},
    #                             status=status.HTTP_400_BAD_REQUEST)
    #         serializer.save()
    #         return Response({"success": True, "status": 201,"data": serializer.data}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({"success": "error", "status" : 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class AddUserImageView(GenericAPIView):
    serializer_class = UserImageSerializer
    # permission_classes = (AllowAny,)

    def get(self, request):
        idealMatch = User.objects.all()
        serializer = UserImageSerializer(idealMatch, many=True)
        return Response({"success": True, "base_url": "http://18.224.254.170/media/","data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):

        serializer = UserImageSerializer(data=request.data)

        if serializer.is_valid():
            # idealmatch = serializer.validated_data['idealmatch']
            # check_name =UserIdealMatch.objects.filter(idealmatch=idealmatch).first()

            # if check_name:
            #     return Response({"message": "idealmatch Already Exists with  This name! "}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddHeigthView(GenericAPIView):
    serializer_class  = HeightSerializer
    # permission_classes = (AllowAny,)

    def get(self, request):
        height = Heigth.objects.all()
        serializer = HeightSerializer(height, many=True)
        return Response({"success": True,   "status" : 200,"data": serializer.data}, status=status.HTTP_200_OK)

    # def post(self, request, format='json'):
    #
    #     serializer = HeightSerializer(data=request.data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"success": True , "status" : 201
    #                             , "data": serializer.data}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    #

class GetUserDetail(GenericAPIView):
    """
    Retrieve, update or delete  a media instance.
    """
    serializer_class = UserDetailSerializer
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        adduserdetail = self.get_object(pk)
        serializer = UserDetailSerializer(adduserdetail)
        return Response({"success": True, "status" : 200 ,"data": serializer.data}, status=status.HTTP_200_OK)



class UserUpdateIdealMatch(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        question = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(question, data=request.data, partial=True)
        question.idealmatch_field = True
        question.save(update_fields=["idealmatch_field"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User Ideal Match field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdatePassion(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        question = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(question, data=request.data, partial=True)
        question.passion_field = True
        question.save(update_fields=["passion_field"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User Passion field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateGender(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        question = get_object_or_404(User, pk=pk)
        serializer = UserGenderSerializer(question, data=request.data, partial=True)
        question.gender_field = True
        question.save(update_fields=["gender_field"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User Gender field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserUpdateInterest(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        question = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(question, data=request.data, partial=True)
        question.interest_in_field = True
        question.save(update_fields=["interest_in_field"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User Gender field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateHight(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        question = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(question, data=request.data, partial=True)
        question.height_field = True
        question.save(update_fields=["height_field"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User height_field field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateLoction(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        question = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(question, data=request.data, partial=True)
        question.location_field = True
        question.save(update_fields=["location_field"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User location field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class UserUpdateMedia(RetrieveUpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def patch(self, request, *args, **kwargs):
#
#         pk = self.kwargs.get('pk')
#         question = get_object_or_404(User, pk=pk)
#         serializer = UserSerializer(question, data=request.data, partial=True)
#         question.is_media_field = True
#         question.save(update_fields=["is_media_field"])
#         if serializer.is_valid():
#             question = serializer.save()
#             return Response({"message" : "User Media field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateMaritalStatus(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        question = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(question, data=request.data, partial=True)
        question.relationship_status_field = True
        question.save(update_fields=["relationship_status_field"])
        if serializer.is_valid():
            question = serializer.save()

            return Response({"message" : "User relationship_status field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDelete(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):

        userdel = self.get_object(pk)
        userdel.delete()
        return Response({'status':204,'message':'User Successfully Deleted!' ,'success':True},status=status.HTTP_204_NO_CONTENT)