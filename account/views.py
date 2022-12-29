# import jwt
import random
import http.client
from django.conf import settings
from DatingApp.baseurl import base_url
from django.http import HttpResponse
from django.contrib.auth import logout
from operator import add
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from datetime import datetime, timedelta
from rest_framework.generics import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.views import *
from account.utils import generate_access_token, generate_refresh_token
from post.serializers import *
from usermedia.serializers import *
from account.models import User
from account.serializers import *
from friend.models import FriendList, FriendRequest
from friend.serializers import *
from usermedia.models import *
from twilio.rest import Client
from masterdata.models import CusztomFCMDevice

def send_otp(mobile, otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    headers = {'content-type': "application/json"}
    url = "http://control.msg91.com/api/sendotp.php?otp=" + otp + "&message=" + \
        "Your otp is " + otp + "&mobile=" + mobile + \
        "&authkey=" + authkey + "&country=91"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None


class LoginApiView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(

        operation_summary="User Login Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User Mobile Number'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='Enter Otp'),
                'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='Add Country Code'),
            }),

        tags=['Account']
    )
    def post(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        try:
            print(request.data)
            mobile = request.data['mobile']
            country_code = request.data['country_code']

            user = User.objects.filter(
                mobile=mobile, country_code=country_code).first()
            # user = User.objects.filter(
            #     mobile=mobile, country_code=country_code, otp=otp).first()
            if user is None:
                return Response(
                    {"message": "mobile no. not registered", "success": False,
                        'is_register': False, "status": 404},
                    status=status.HTTP_404_NOT_FOUND)
            # otp = str(random.randint(999, 9999))
            # if user.is_active == True:
            otp = 1234
            user.otp = otp
            user.save()
            if "fcm_token" in request.data:
                json = request.data
                if  CusztomFCMDevice.objects.filter(user=user).first():
                    ass = CusztomFCMDevice.objects.filter(user=user).first()
                    if ass.registration_id:
                        ass.registration_id= json['fcm_token']
                        ass.save()
                    else :
                        device = CusztomFCMDevice()
                        device.registration_id = json['fcm_token']
                        device.type = json['device_type']
                        device.name = "anroide"
                    
                        device.user=user
                        device.save()

                else:
                    fcm_token = json['fcm_token']

                    device = CusztomFCMDevice.objects.filter(user=user)
                    if device:
                        device.registration_id = fcm_token
                        device.type = json['device_type']
                        device.name = " User"
                    
                        device.user=user
                        device.save()
                    else :
                        device = CusztomFCMDevice()
                        device.registration_id = fcm_token
                        device.type = json['device_type']
                        device.name = "User"
                    
                        device.user=user
                        device.save()
                            
                fcm_data = CusztomFCMDevice.objects.filter(user=user).first()
                if fcm_data:
                    datafcm = fcm_data.registration_id
                else :
                    # json = request.data
                    # fcm_token = json['fcm_token']
                    # device = CusztomFCMDevice()
                    # device.registration_id = fcm_token
                    # device.type = json['device_type']
                    # device.name = "User"
                
                    # device.user=user
                    # device.save()
                    datafcm = ""

            return Response({'base_url':base_url,"message": "User Login Successfully!", "status": 200, "success": True, 'is_register': True, "user": {
                'id': user.id,
                'email': user.email,
                'mobile': user.mobile,
                'country_code': user.country_code,
                'otp': user.otp,
                'name': user.name,
                # 'profile_image':user.profile_image.url,
                'is_verified': user.is_verified,
                "fcm_token" : datafcm
                }},
                status=status.HTTP_200_OK)
            # else:
            #     return Response({'success': False, "status": 200, 'message': 'user is inactive',
            #                      "data": user.active_reseaon},
            #                     status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'success': False, "status": 404, 'message': 'Data Not Found'},
                            status=status.HTTP_404_NOT_FOUND)


class RegistrationApiView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    @swagger_auto_schema(

        operation_summary="User Registration Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User Mobile Number'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='User Name'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='Add Otp'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User Email'),
                'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='User Country Code'),
                'birth_date': openapi.Schema(type=openapi.TYPE_STRING, description='Date of Birth must be in YYYY-MM-DD format.'),

            }),


        tags=['Account']
    )
    def post(self, request):
        

        try:
            
            email = request.data['email']
            mobile = request.data['mobile']
            country_code = request.data['country_code']
            
            name = request.data['name']
            birth_date = request.data['birth_date']
            check_mobile = User.objects.filter(mobile=mobile).first()
            check_email = User.objects.filter(email=email).first()
            print("request.data",request.data)
            if check_mobile:
            #     if check_mobile.is_verified == False :

            #         if check_email:
            #             if check_mobile.is_verified == True :
            #                 return Response(
            #             {"message": "email Already Exists", 'success': False,
            #                 'status': 400, 'is_register': False, "email": email},
            #         status=status.HTTP_400_BAD_REQUEST)
            #         otp = str(random.randint(1000, 9999))
            # # otp = str(1234)
            #         account_sid = 'ACbcfad7f1219fdaac963471693bafdf61'
            #         auth_token = 'a7ed817c4cff17e72b7508c320ce0f66'
            #         client = Client(account_sid, auth_token)

            #         message = client.messages.create(
            #                                     body=f'Hi, your test result is {otp} . Great job',
            #                                     from_=+19035183066,
            #                                     to=+919131897782
            #                                 )

            #         print("Otp from tiwillo",message.sid)
            #         print("otp", otp)
            #         if profile_image :
            #             val = User.objects.get(mobile=mobile)
            #             val.email = email,
            #             val.email=email, 
            #             val.name=name, 
            #             val.birth_date=birth_date, 
            #             val.mobile=mobile, otp=otp
            #             val.profile_image = profile_image
                        
            #             val.save()
            #         else : 
            #             val = User.objects.get(mobile=mobile)
            #             val.email = email,
            #             val.email=email, 
            #             val.name=name, 
            #             val.birth_date=birth_date, 
            #             val.mobile=mobile, otp=otp
            #             val.save()
            #         # print(type(user))
            #         # user.save()
            #         return Response({"message": "Your Registrations is successfully", "status": 201, "success": True, 'is_register': True,
            #                         "user": {
            #                             'id': user.id,
            #                             'email': user.email,
            #                             'mobile': user.mobile,
            #                             'country_code': user.country_code,
            #                             'name': user.name,
            #                             'otp': user.otp,
            #                             #  'profile_image':user.profile_image,
            #                             'is_verified': user.is_verified}},
            #                         status=status.HTTP_201_CREATED)   
            #     else :
                
                return Response(
                    {"message": "Mobile Number Already Exists!", 'status': 400,
                        'success': False, 'is_register': False, "mobile": mobile},
                    status=status.HTTP_400_BAD_REQUEST)
            if check_email:
                return Response(
                    {"message": "email Already Exists", 'success': False,
                        'status': 400, 'is_register': False, "email": email},
                    status=status.HTTP_400_BAD_REQUEST)

            otp = str(random.randint(1000, 9999))
            # otp = str(1234)
            account_sid = 'ACbcfad7f1219fdaac963471693bafdf61'
            auth_token = 'a7ed817c4cff17e72b7508c320ce0f66'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                                        body=f'Hi, your test result is {otp} . Great job',
                                        from_=+19035183066,
                                        to=+919131897782
                                    )

            print("Otp from tiwillo",message.sid)
            print("otp", otp)
            if 'profile_image' in request.data :
                profile_image = request.data['profile_image']
                if profile_image is None:

                

                    user = User(email=email, name=name, birth_date=birth_date, mobile=mobile, otp=otp,
                            country_code=country_code,profile_image=profile_image)
                else : 
                    user = User(email=email, name=name, birth_date=birth_date, mobile=mobile, otp=otp,
                            country_code=country_code,profile_image=profile_image)
            # print(type(user))
            user.save()
            json = request.data
            if 'fcm_token' in json:
                fcm_token = json['fcm_token']
                user = user 
                device = CusztomFCMDevice()
                device.registration_id = fcm_token
                device.type =request.POST['device_type']
                device.name = "abc"
                device.user = user
                device.save()

                print("device",device.registration_id)
            fcm_data = CusztomFCMDevice.objects.filter(user=user).first()
            if fcm_data:
                datafcm = fcm_data.registration_id
            else :
                datafcm = ""




            return Response({"message": "Your Registrations is successfully", 'base_url':base_url,"status": 201, "success": True, 'is_register': True,
                             "user": {
                                 'id': user.id,
                                 'email': user.email,
                                 'mobile': user.mobile,
                                 'country_code': user.country_code,
                                 'name': user.name,
                                 'otp': user.otp,
                                #  'profile_image':user.profile_image,
                                 'is_verified': user.is_verified,
                                 'datafcm':datafcm
                                 }},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'success': False,  'status': 400,  'message': 'User Not Register', 'is_register': False},
                            status=status.HTTP_400_BAD_REQUEST)


class UserDataApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserProfileSerializer

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="User Detail Profile Time Line Api",
        tags=['Account']
    )
    def get(self, request, user_id, format=None):

        register_user = request.user.id
       
        user = User.objects.get(id=user_id)
        post = PostUpload.objects.filter(user_id=user_id)
        media = MediaPost.objects.filter(user_id=user_id)
        follow = FollowRequest.objects.filter(user_id=user_id)
        followaccept = FollowRequest.objects.filter(follow_id=user_id)
        # friendrequest = FriendRequest.objects.filter(user_id=user_id)
        # friendaccept = FriendList.objects.filter(user_id=user_id)
        userserializer = UserProfileSerializer(user, context={
             'request': request,'request1': register_user})

        postserializer = PostUploadSerializers(post, many=True)
        follow_serializer = FollowRequestFollowingSerializer(follow, many=True)
        follow_accept_serializer = FollowRequestFollowerV2Serializer(
            followaccept, context={
            'request': request.user.id}, many=True)
        mediaserializer = GetMediaPostSerializers(media, many=True)
        # friend_req_serializer = FriendRequestSerializer(
        #     friendrequest, many=True)
        # friend_acc_serializer = FriendListUserSerializer(
        #     friendaccept, many=True)

        return Response({"base_url": base_url,
                        "user": userserializer.data,
                         "PostCount": len(postserializer.data),
                         "post": postserializer.data,
                        #  "friendaccept": friend_acc_serializer.data,
                        #  "friendrequest": friend_req_serializer.data,
                        #  "MediaCount": len(mediaserializer.data),
                         "media": mediaserializer.data,
                         "Following": len(follow_serializer.data),
                         "Follower": len(follow_accept_serializer.data),
                         "success": True,
                         "message": "User  Profile TimeLine!",
                         "status": 200,
                         },
                        status=status.HTTP_200_OK)


class UserUpdate(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(

        operation_summary="User Update Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile no'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='User name'),
            }),

        tags=['Account']
    )
    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        # object = User.objects.get(user_id=user_id)

        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)

        if serializer.is_valid():
            question = serializer.save()

            return Response({"message": "User Data is Successfully Updated!", "status": 200, "success": True, "data": UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserDetail(GenericAPIView):

    permission_classes = [AllowAny, ]
    """
    Retrieve, update or delete  a media instance.
    """
    serializer_class = UserDetailSerializer

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(

        operation_summary=" Get User Detail",
        tags=['Account']
    )
    def get(self, request, user_id, format=None):

        adduserdetail = self.get_object(user_id)
        serializer = UserDetailSerializer(adduserdetail)
        return Response({"success": True, "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)


class UserUpdateIdealMatch(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(

        operation_summary="User Add Ideal Match Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'idealmatch': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Idealmatch'),

            }),

        tags=['Account']
    )
    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)
        question.is_idealmatch = True
        question.save(update_fields=["is_idealmatch"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message": "User Ideal Match field is Successfully Updated!", "status": 200, "success": True, "data": UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateProfileApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(

        operation_summary="User Update Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'passion': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Passion'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Gender'),
                'idealmatch': openapi.Schema(type=openapi.TYPE_STRING, description='Add User IdealMatch'),
                'marital_status': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Marital Status'),
                'tall': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Height'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Location'),
                'interest_in': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Interest In'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Email'),


            }),

        tags=['Account']
    )
    def patch(self, request, user_id, *args, **kwargs):
        # user_id = request.user.id
        user_id = self.kwargs.get('user_id')
        user_data = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user_data, data=request.data)

        if 'gender' in request.data:
            user_data.is_gender = True
            user_data.save(update_fields=["is_gender"])

        if 'passion' in request.data:
            user_data.is_passion = True
            user_data.save(update_fields=["is_passion"])

        if 'idealmatch' in request.data:
            user_data.is_idealmatch = True
            user_data.save(update_fields=["is_idealmatch"])

        if 'interest_in' in request.data:
            user_data.is_interest_in = True
            user_data.save(update_fields=["is_interest_in"])

        if 'location' in request.data:
            user_data.is_location = True
            user_data.save(update_fields=["is_location"])

        if 'tall' in request.data:
            user_data.is_tall = True
            user_data.save(update_fields=["is_tall"])

        if 'marital_status' in request.data:
            user_data.is_marital_status = True
            user_data.save(update_fields=["is_marital_status"])

        if serializer.is_valid():
            user_data = serializer.save()
            return Response({"message": "User Profile is Successfully Updated!", "status": 200, "success": True, "data": UserSerializer(user_data).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyApiView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(

        operation_summary="User Otp Verify Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User Mobile No'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='Add Otp'),
                'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='Add Country Code'),
            }),

        tags=['Account']
    )
    def post(self, request):
        try:
          
            mobile = request.data['mobile']
            otp = request.data['otp']
            country_code = request.data['country_code']
            mobile = int(mobile)
            otp = int(otp)

            user_obj = User.objects.get(
                mobile=mobile, otp=otp, country_code=country_code)
            # print( user_obj.id)
            # user_obj =user_obj.id
            user_obj_otp = int(user_obj.otp)
            if user_obj_otp == otp:

                user_obj.is_verified = True
                access_token = generate_access_token(user_obj)
                refresh_token = generate_refresh_token(user_obj)

                # response.set_cookie(self, key='refreshtoken',
                #                     value=refresh_token, httponly=True)
                # print(refresh_token)
                user_obj.auth_tokens = access_token
                # user_obj.save()
                if (user_obj.is_gender and user_obj.is_passion and user_obj.is_tall and
                        user_obj.is_interest_in and user_obj.is_idealmatch and user_obj.is_marital_status) == True:
                    user_obj.is_complete_profile = True
                    user_obj.save()
                else:
                    user_obj.is_complete_profile = False
                    user_obj.save()

                return Response(
                    {'success': True, 'message': 'your OTP is verified', 'status': 200, 'is_register': True, "token": access_token, "user": {
                        'id': user_obj.id,
                        'email': user_obj.email,
                        'mobile': user_obj.mobile,
                        'country_code': user_obj.country_code,
                        'name': user_obj.name,
                        "is_complete_profile": user_obj.is_complete_profile,
                        'is_verified': user_obj.is_verified,
                        "is_register_user_verified":user_obj.is_register_user_verified, }

                     },
                    status=status.HTTP_200_OK)
            return Response({'success': "success", 'message': 'Wrong OTP', "status": 404, "data": serializers.data},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
        return Response(
            {'success': False, 'message': ' Wrong OTP',
                'status': 404, 'is_register': False},
            status=status.HTTP_404_NOT_FOUND)


class GetUserDetailApiView(GenericAPIView):

    """
    Retrieve, Checklist Api.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserDetailSerializer

    @swagger_auto_schema(
        operation_summary=" Get User Detail(Checklist Api)",
        tags=['Account']
    )
    def get(self, request,  format=None):

        req = request.user
        # req.is_media = True
        if (req.is_gender and req.is_passion and req.is_tall and
                req.is_interest_in and req.is_idealmatch and req.is_marital_status and req.is_media) == True:
            req.is_complete_profile = True
            req.save()
        else:
            req.is_complete_profile = False
            req.save()

        serializer = UserDetailSerializer(req)
        return Response({"success": True, "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)


class LogoutApiView(APIView):
    permission_class = [IsAuthenticated, ]

    @swagger_auto_schema(

        operation_summary=" Api for User Logout ",

        tags=['Account']
    )
    def get(self, request, format=None):
        # simply delete the token to force a login
        user = User.objects.get(id=request.user.id)

        user.auth_tokens = ''
        user.save()
        # print(user.auth_tokens.delete())
        logout(request)
        return Response({'message': "Successfully LogOut", 'status': 200, 'success': True}, status=status.HTTP_200_OK)


class UserVerifiedApiView(GenericAPIView):

    """
    User Verification Api.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserVerifiedSerializer
    # permission_classes = [IsAuthenticated,]

    # def get_object(self, user_id):
    #     try:
    #         return User.objects.get(id=user_id)
    #     except User.DoesNotExist:
    #         raise Http404

    @swagger_auto_schema(

        operation_summary=" Api for User Verified ",

        tags=['Account']
    )
    def get(self, request, format=None):

        # adduserdetail = self.get_object(user_id)

        req = User.objects.get(id=request.user.id)
        if req.user_verified_status == 2:

            print (req.user_verified_status)
            serializer = UserVerifiedSerializer(req)
            return Response({"success": True, "status": 200, "message":"Account Verified Succefully","data": serializer.data}, status=status.HTTP_200_OK)
        elif req.user_verified_status == 1:
            serializer = UserVerifiedSerializer(req)
            return Response({"success": True, "status": 200, "message":"Please Wait For Verification","data": serializer.data}, status=status.HTTP_200_OK)
        else :
            serializer = UserVerifiedSerializer(req)
            return Response({"success": True, "status": 200, "message":"Please add you Document","data": serializer.data}, status=status.HTTP_200_OK)
        
class UserVerifyDocumentApi(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserVerifyDocSerializer

    @swagger_auto_schema(

        operation_summary="User Update Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={

                'selfie': openapi.Schema(type=openapi.TYPE_STRING, description='Add User selfie'),
                'govt_id': openapi.Schema(type=openapi.TYPE_STRING, description='Add User govt_id'),

            }),

        tags=['Account']
    )
    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        # user_id = self.kwargs.get('user_id')
        print("UserVerifyDocumentApi",request.data)
        user_data = get_object_or_404(User, id=user_id)
        serializer = UserVerifyDocSerializer(user_data, data=request.data)
        
        if serializer.is_valid():
            user_data.user_verified_status = 1
            user_data.save(update_fields=["user_verified_status"])
            user_data = serializer.save()

            return Response({"message": "User Document successfully added!", "status": 200, "success": True,
                             "doc_data": serializer.data, "data": UserSerializer(user_data).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserVerifyDocumentApi(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserVerifyDocSerializer

    def get(self, request):
        user_id = request.user.id
        userInterest =User.objects.filter(id=user_id)
        serializer = UserVerifyDocSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data,'base_url':base_url}, status=status.HTTP_200_OK)


class ResendOtpApiView(GenericAPIView):
    permission_classes = [AllowAny, ]
    # queryset = User.objects.all()
    serializer_class = UserResendOtpSerializer

    @swagger_auto_schema(

        operation_summary="Resend Otp Api",
        tags=['Account']
    )
    def post(self, request, *args, **kwargs):
        get_mobile = request.data['mobile']
        get_country = request.data['country_code']

        # if User.objects.filter(id=get_user).exists() and not User.objects.get(username=get_user).is_active:
        if User.objects.filter(mobile=get_mobile).exists():
            get_user = User.objects.filter(
                mobile=get_mobile, country_code=get_country)

            user = User.objects.get(mobile=get_mobile)
            user_otp = random.randint(1000, 9999)

            user.otp = user_otp
            user.save(update_fields=["otp"])
            # User.objects.update(otp=user_otp)
            mess = f"Hello, {user.name}, \nYour OTP is {user_otp}\n Thanks!"
            print(mess)
            # send_mail(
            #     "Welcome to Solve Litigation - Verify your Email",  # subject
            #     mess,  # message
            #     settings.EMAIL_HOST_USER,  # sender
            #     [user.email],  # receiver
            #     fail_silently=False
            # )
            return Response({"message": " Successfully Resend Otp", "status": 200, "success": True,
                            "data": {
                                "otp": user.otp,
                                "user": user.name,
                                "mobile": user.mobile
                            }
            }, status=status.HTTP_200_OK)

        return Response({"message": " No Resend otp", "status": 200, "success": True,
                         }, status=status.HTTP_200_OK)


class SettingPrivacyApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    # queryset = User.objects.all()
    serializer_class = UserSettingSerializer

    @swagger_auto_schema(
        operation_summary="Setting Privacy Update",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'show_profile': openapi.Schema(type=openapi.TYPE_STRING, description='update user profile by Flag 0 for EveryOne, 1 for Friend and 2 for OnlyMe'),
                'show_friend': openapi.Schema(type=openapi.TYPE_STRING, description='update Friend by Flag 0 for EveryOne, 1 for Friend and 2 for OnlyMe'),
                'show_public_post': openapi.Schema(type=openapi.TYPE_STRING, description='update Public post by Flag 0 for EveryOne, 1 for Friend and 2 for OnlyMe'),
                'show_private_post': openapi.Schema(type=openapi.TYPE_STRING, description='update Private by Flag 0 for EveryOne, 1 for Friend and 2 for OnlyMe'),
                'show_media_photo': openapi.Schema(type=openapi.TYPE_STRING, description='update Media Post Flag 0 for EveryOne, 1 for Friend and 2 for OnlyMe'),
                'show_media_video': openapi.Schema(type=openapi.TYPE_STRING, description='update Media Video by Flag 0 for EveryOne, 1 for Friend and 2 for OnlyMe'),
            }),
        tags=['Account']
    )
    def put(self, request, *args, **kwargs):

        user_data = get_object_or_404(User, id=request.user.id)

        serializer = UserSettingSerializer(user_data, data=request.data)
        print("request.data", request.data)

        if 'show_profile' in request.data:
            user_data.show_profile = request.data["show_profile"]
            user_data.save(update_fields=["show_profile"])

        if 'show_public_post' in request.data:
            user_public_post = PostUpload.objects.filter(
                user=request.user.id, is_private=0)
            for i in range(len(user_public_post)):

                # user_public_post[i]
                user_public_post[i].show_public_post = request.data["show_public_post"]
                user_public_post[i].save(update_fields=["show_public_post"])

        if 'show_private_post' in request.data:
            
            user_private_post = PostUpload.objects.filter(
                user=request.user.id, is_private=1)
            
            for i in range(len(user_private_post)):  
                user_private_post[i].show_private_post = request.data["show_private_post"]
                user_private_post[i].save(update_fields=["show_private_post"])
    

        if 'show_media_video' in request.data:
            user_media_video = MediaVideo.objects.filter(
                user=request.user.id)
           
            for i in range(len(user_media_video)):

                user_media_video[i].show_media_video = request.data["show_media_video"]
                user_media_video[i].save(update_fields=["show_media_video"])

        if 'show_media_photo' in request.data:
            user_media_photo = MediaPost.objects.filter(
                user=request.user.id)
            for i in range(len(user_media_photo)):
                user_media_photo[i].show_media_photo = request.data["show_media_photo"]
                user_media_photo[i].save(update_fields=["show_media_photo"])

        if 'show_friend' in request.data:
            user_friend = FriendList.objects.filter(user=request.user.id)
            for i in range(len(user_friend)):
                user_friend[i].show_friend = request.data["show_friend"]
                user_friend[i].save(update_fields=["show_friend"])

        # if serializer.is_valid():
        #     user_data = serializer.save()
        return Response({"message": "User setting privacy updated", "status": 200, "success": True,
                         "data": UserSettingSerializer(user_data).data})
        # return Response({"message": "No data Found", }, status=status.HTTP_400_BAD_REQUEST)


class UserCreateView(GenericAPIView):
    serializer_class = RegisterSerializer
    """
    Creates the user.
    """
    @swagger_auto_schema(

        operation_summary="User Otp Verify Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile no'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='User name'),
            }),

        tags=['Account']
    )
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
                                 "msg": msg}, status=status.HTTP_201_CREATED)
            else:
                return Response({"data": serializer.errors, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data": serializer.errors, "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class UserDataV2(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = (UserSerializer)

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get_serializer_context(self):

        user = self.request.user
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    @swagger_auto_schema(

        operation_summary="User Detail Profile Time Line Api",
        # request_body=openapi.Schema(
        # type=openapi.TYPE_OBJECT,
        # properties={
        #     'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile no'),
        #     'name': openapi.Schema(type=openapi.TYPE_STRING, description='User name'),
        # }),

        tags=['Account']
    )
    def get(self, request, format=None):

        user_id = request.user.id
        user = User.objects.get(id=user_id)
        post = PostUpload.objects.filter(user_id=user_id)
        media = MediaPost.objects.filter(user_id=user_id)
        follow = FollowRequest.objects.filter(user_id=user_id)
        followaccept = FollowRequest.objects.filter(follow_id=user_id)
        friendrequest = FriendRequest.objects.filter(user_id=user_id)
        friendaccept = FriendList.objects.filter(user_id=user_id)

        userserializer = UserSerializer(user)
        postserializer = PostUploadV2Serializers(
            post, context={'request': request}, many=True)
        follow_serializer = FollowRequestFollowingSerializer(follow, many=True)
        follow_accept_serializer = FollowRequestFollowerV2Serializer(
            followaccept, many=True)
        mediaserializer = GetMediaV2PostSerializers(
            media, context={'request': request}, many=True)
        friend_req_serializer = FriendRequestSerializer(
            friendrequest, many=True)
        friend_acc_serializer = FriendListUserSerializer(
            friendaccept, many=True)

        return Response({
            "user": userserializer.data,
            "PostCount": len(postserializer.data),
            "post": postserializer.data,
            "friendaccept": friend_acc_serializer.data,
            "friendrequest": friend_req_serializer.data,
            "MediaCount": len(mediaserializer.data),
            "media": mediaserializer.data,
            "Following": len(follow_serializer.data),
            "Follower": len(follow_accept_serializer.data),
            "success": True,
            "message": "User  Profile TimeLine!",
            "status": 200,
        },
            status=status.HTTP_200_OK)


class UserUpdateMaritalStatus(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(

        operation_summary="Add User Marital Status Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'marital_status': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Marital Status'),

            }),

        tags=['Account']
    )
    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)
        question.is_merital_status = True
        question.save(update_fields=["is_merital_status"])
        if serializer.is_valid():
            question = serializer.save()

            return Response({"message": "User Marital Status field is Successfully Updated!", "status": 200, "success": True, "data": UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateProfileV2(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(

        operation_summary="User Update Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'passion': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Passion List'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Gender'),
                'idealmatch': openapi.Schema(type=openapi.TYPE_STRING, description='Add User IdealMatch'),
                'marital_status': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Marital Status'),
                'tall': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Height'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Location'),
                'interest_in': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Interest In'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Email'),

            }),

        tags=['Account']
    )
    def put(self, request, *args, **kwargs):
        
        user_id = request.user.id
        # user_id = self.kwargs.get('user_id')
        user_data = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user_data, data=request.data,partial=True)
        print("request.data", request.data)
        # if 'user_media' in request.FILES.getlist('user_media')
        # user = UserProfile.objects.get(id=user_id)
        # profile_im = request.FILES["profile_image"]
        
        # user.profile_image= profile_im
        # user.save()
        if 'gender' in request.data:
            user_data.is_gender = True
            user_data.save(update_fields=["is_gender"])
        
        if 'birth_date' in request.data:
            user_data.birth_date = request.data['birth_date']
            user_data.save(update_fields=["birth_date"])

        if 'passion' in request.data:
            user_data.is_passion = True
            user_data.save(update_fields=["is_passion"])

        if 'idealmatch' in request.data:
            user_data.is_idealmatch = True
            user_data.save(update_fields=["is_idealmatch"])

        if 'interest_in' in request.data:
            user_data.is_interest_in = True
            user_data.save(update_fields=["is_interest_in"])

        if 'location' in request.data:
            user_data.is_location = True
            user_data.save(update_fields=["is_location"])
     
        if 'tall' in request.data:
            user_data.is_tall = True
            user_data.save(update_fields=["is_tall"])

        if 'marital_status' in request.data:
            user_data.is_marital_status = True
            user_data.save(update_fields=["is_marital_status"])

        if serializer.is_valid():
            user_data = serializer.save()
            return Response({"message": "User Profile is Successfully Updated!", "status": 200, "success": True,
                             "data": UserSerializer(user_data).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateGender(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(

        operation_summary="Add User Gender Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Gender'),

            }),

        tags=['Account']
    )
    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserGenderSerializer(question, data=request.data)
        question.is_gender = True
        question.save(update_fields=["is_gender"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message": "User Gender field is Successfully Updated!", "status": 200, "success": True, "data": UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateInterest(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(

        operation_summary="Add User Interest Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'interest_is': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Intrest In'),

            }),

        tags=['Account']
    )
    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)
        question.is_interest_in = True
        question.save(update_fields=["is_interest_in"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message": "User IntrestIn field is Successfully Updated!", "status": 200, "success": True, "data": UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateHight(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(

        operation_summary="Add User Height Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tall': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Height'),

            }),

        tags=['Account']
    )
    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)
        question.is_tall = True
        question.save(update_fields=["is_tall"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message": "User Tall field is Successfully Updated!", "status": 200, "success": True, "data": UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDelete(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="User delete by Id",

        operation_summary="Delete User  Api",

        tags=['Account']
    )
    def delete(self, request, user_id, format=None):

        userdel = self.get_object(user_id)
        userdel.delete()
        return Response({'status': 204, 'message': 'User Successfully Deleted!', 'success': True}, status=status.HTTP_204_NO_CONTENT)


class UserProfileMediaEditAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="Get Api For User Edit",
        tags=['Account']
    )
    def get(self, request, *args, **kwargs):
        user_data = get_object_or_404(User, id=request.user.id)
        user_edit_data = MediaPost.objects.filter(user_id=request.user.id)

        serializer = UserSerializer(user_data,)
        user_edit = UserMediaEditSerializer(user_edit_data, many=True)

        return Response({"message": "Get Data For User Edit", "status": 200, "success": True,
                         "data": serializer.data, 'media': user_edit.data}, status=status.HTTP_200_OK)


class OTPVerifyV2(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(

        operation_summary="User Otp Verify Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile no'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='otp'),
                'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='country_code'),
            }),

        tags=['Account']
    )
    def post(self, request):

        try:
            mobile = request.data['mobile']
            otp = request.data['otp']
            country_code = request.data['country_code']
            mobile = int(mobile)
            otp = int(otp)

            user_obj = User.objects.get(
                mobile=mobile, otp=otp, country_code=country_code)
            # print( user_obj.id)
            # user_obj =user_obj.id
            user_obj_otp = int(user_obj.otp)

            if user_obj_otp == otp:

                user_obj.is_verified = True

                # user_obj.save()
                if (user_obj.is_gender and user_obj.is_passion and user_obj.is_tall and user_obj.is_location and
                        user_obj.is_interest_in and user_obj.is_idealmatch and user_obj.is_marital_status ) == True:
                    # is_complete_profile = True
                    # if (user_obj.is_gender and user_obj.is_passion and user_obj.is_tall and user_obj.is_location and
                    #     user_obj.is_interest_in and user_obj.is_idealmatch and user_obj.is_marital_status and user_obj.is_media) == True:
                    # # is_complete_profile = True
                    user_obj.is_complete_profile = True

                    user_obj.save()

                else:
                    # is_complete_profile = False
                    user_obj.is_complete_profile = False
                    user_obj.save()

                return Response(
                    {'success': True, 'message': 'your OTP is verified', 'status': 200, 'is_register': True, "user": {
                        'id': user_obj.id,
                        'email': user_obj.email,
                        'mobile': user_obj.mobile,
                        'country_code': user_obj.country_code,
                        'name': user_obj.name,
                        "is_complete_profile": user_obj.is_complete_profile,
                        'is_verified': user_obj.is_verified, }

                     },
                    status=status.HTTP_200_OK)
            return Response({'success': "success", 'message': 'Wrong OTP', "status": 404, "data": serializers.data},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
        return Response(
            {'success': False, 'message': ' Wrong otp',
                'status': 404, 'is_register': False},
            status=status.HTTP_404_NOT_FOUND)
