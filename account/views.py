# import jwt
import http.client
from operator import add
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from rest_framework import viewsets
from rest_framework.generics import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.views import *
from post.serializers import *
from usermedia.serializers import *
from .models import *
from .serializers import *
from friend.models import *
from friend.serializers import *
from account.utils import generate_access_token, generate_refresh_token



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
    @swagger_auto_schema(
      
        operation_summary = "User Login Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile no'),
            'otp': openapi.Schema(type=openapi.TYPE_STRING, description='Enter Otp'),
            'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='Add Country Code'),
        }),

        tags = ['Account']
    )
   
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


class Registration(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    @swagger_auto_schema(
      
        operation_summary = "User Regitration Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile no'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='User name'),
            'otp': openapi.Schema(type=openapi.TYPE_STRING, description='Add Otp'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='country code'),
            'birth_date': openapi.Schema(type=openapi.TYPE_STRING, description=' date of birth must be in YYYY-MM-DD format.'),
            

        }),
        

        tags = ['Account']
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
            # print(type(user))
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
    @swagger_auto_schema(
      
        operation_summary = "User Otp Verify Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile no'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='User name'),
        }),

        tags = ['Account']
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
                                 "msg": msg},status =status.HTTP_201_CREATED)
            else:
                return Response({"data": serializer.errors,"status": 400 }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"data": serializer.errors,"status": 400}, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework_jwt.settings import api_settings
class OTPVerifyV2(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    @swagger_auto_schema(
      
        operation_summary = "User Otp Verify Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile no'),
            'otp': openapi.Schema(type=openapi.TYPE_STRING, description='otp'),
            'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='country_code'),
        }),

        tags = ['Account']
    )

    def post(self, request):

        try:
            mobile = request.data['mobile']
            otp = request.data['otp']
            country_code = request.data['country_code']
            mobile = int(mobile)
            otp = int(otp)

            user_obj = User.objects.get(mobile=mobile, otp=otp, country_code=country_code)
            # print( user_obj.id)
            # user_obj =user_obj.id
            user_obj_otp = int(user_obj.otp)

            if user_obj_otp == otp:

                user_obj.is_phone_verified = True


                user_obj.save()
                if (user_obj.is_gender and user_obj.is_passion and user_obj.is_tall  and user_obj.is_location and
                    user_obj.is_interest_in and user_obj.is_idealmatch and user_obj.is_marital_status  and user_obj.is_media) == True:
                    is_complete_profile = True
                else :
                    is_complete_profile = False

                return Response(
                    {'success': True, 'message': 'your OTP is verified', 'status': 200,'is_register': True ,"user": {
                        'id': user_obj.id,
                        'email': user_obj.email,
                        'mobile': user_obj.mobile,
                        'country_code': user_obj.country_code,
                        'name': user_obj.name,
                        "is_complete_profile": is_complete_profile,
                        'is_verified': user_obj.is_verified, }

                     },
                    status=status.HTTP_200_OK)
            return Response({'success': "success", 'message': 'Wrong OTP', "status": 404,"data": serializers.data},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
        return Response(
            {'success': False, 'message': ' Mobile Number Not Registered','status': 404, 'is_register': False},
            status=status.HTTP_404_NOT_FOUND)


class UserData(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = (UserSerializer )


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
        friendrequest = FriendRequest.objects.filter(receiver_id=user_id)
        friendaccept = FriendList.objects.filter(user_id=user_id)

        userserializer = UserSerializer(user)
        postsrializer = PostUploadSerializers(post,context={'request': request} ,many=True)
        followserializer = FollowRequestFollowingSerializer(follow, many=True)
        followacceptserializer = FollowRequestFollowerV2Serializer(followaccept, many=True)
        mediaserializer = GetMediaPostSerializers(media,context={'request': request}, many=True)
        friendreqserializer = FriendRequestSerializer(friendrequest, many=True)
        friendaccserializer = FriendListUserSerializer(friendaccept, many=True)

        return Response({
                        "user": userserializer.data,
                         "PostCount": len(postsrializer.data),
                         "post": postsrializer.data,
                         "friendaccept":friendaccserializer.data ,######
                         "friendrequest":friendreqserializer.data,
                         "MediaCount": len(mediaserializer.data),
                         "media": mediaserializer.data,
                         "Following": len(followserializer.data),
                         "Follower": len(followacceptserializer.data),
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
      
        operation_summary = "User Update Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'mobile': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile no'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='User name'),
        }),

        tags = ['Account']
    )

    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        # object = User.objects.get(user_id=user_id)

        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)

        if serializer.is_valid():
            question = serializer.save()

            return Response({"message" : "User Data is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class GetUserDetail(GenericAPIView):

    permission_classes = (IsAuthenticated,)
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
      
        operation_summary = " Get User Detail",
        

        tags = ['Account']
    )
    def get(self, request, user_id, format=None):

        adduserdetail = self.get_object(user_id)
        serializer = UserDetailSerializer(adduserdetail)
        return Response({"success": True, "status" : 200 ,"data": serializer.data}, status=status.HTTP_200_OK)



class UserUpdateIdealMatch(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @swagger_auto_schema(
      
        operation_summary = "User Add Ideal Match Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'idealmatch': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Idealmatch'),
            
        }),

        tags = ['Account']
    )

    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)
        question.is_idealmatch = True
        question.save(update_fields=["is_idealmatch"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User Ideal Match field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateProfile(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @swagger_auto_schema(
      
        operation_summary = "User Update Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'passion': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Passion'),
            'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Gender'),
            'idealmatch': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Idealmatch'),
            'marital_status': openapi.Schema(type=openapi.TYPE_STRING, description='Add User marital_status'),
            'tall': openapi.Schema(type=openapi.TYPE_STRING, description='Add User tall'),
            'location': openapi.Schema(type=openapi.TYPE_STRING, description='Add User location'),
            'interest_in': openapi.Schema(type=openapi.TYPE_STRING, description='Add User interest_in'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Add User email'),
            
            
        }),

        tags = ['Account']
    )

    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        # user_id = self.kwargs.get('user_id')
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
            return Response({"message" : "User Profile is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(user_data).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateGender(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @swagger_auto_schema(
      
        operation_summary = "Add User Gender Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Gender'),
           
        }),

        tags = ['Account']
    )

    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserGenderSerializer(question, data=request.data)
        question.is_gender = True
        question.save(update_fields=["is_gender"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User Gender field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserUpdateInterest(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @swagger_auto_schema(
      
        operation_summary = "Add User Interest Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'interest_is': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Intrest In'),
           
        }),

        tags = ['Account']
    )

    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)
        question.is_interest_in = True
        question.save(update_fields=["is_interest_in"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User InrestIn field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateHight(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @swagger_auto_schema(
      
        operation_summary = "Add User Height Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'tall': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Height'),
           
        }),

        tags = ['Account']
    )

    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)
        question.is_tall = True
        question.save(update_fields=["is_tall"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User Tall field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateLoction(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @swagger_auto_schema(
      
        operation_description="POST description override using decorator",
        operation_summary = "Add User Location Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'location': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Loction'),
           
        }),

        tags = ['Account']
    )
    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)
        question.is_location = True
        question.save(update_fields=["is_location"])
        if serializer.is_valid():
            question = serializer.save()
            return Response({"message" : "User location field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateMaritalStatus(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @swagger_auto_schema(
      
        operation_summary = "Add User Marital Status Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'marital_status': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Marital Status'),
           
        }),

        tags = ['Account']
    )

    def put(self, request, *args, **kwargs):

        user_id = self.kwargs.get('user_id')
        question = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(question, data=request.data)
        question.is_merital_status = True
        question.save(update_fields=["is_merital_status"])
        if serializer.is_valid():
            question = serializer.save()

            return Response({"message" : "User Marital Status field is Successfully Updated!", "status":200,"success":True , "data":UserSerializer(question).data})
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

        operation_summary = "Delete User  Api",
       
        tags = ['Account']
    )


    def delete(self, request, user_id, format=None):

        userdel = self.get_object(user_id)
        userdel.delete()
        return Response({'status':204,'message':'User Successfully Deleted!' ,'success':True},status=status.HTTP_204_NO_CONTENT)


class OTPVerify(GenericAPIView):
    permission_classes= [AllowAny]
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

            user_obj = User.objects.get(mobile=mobile, otp=otp, country_code=country_code)
            # print( user_obj.id)
            # user_obj =user_obj.id
            user_obj_otp  = int(user_obj.otp)
            if user_obj_otp == otp:

                user_obj.is_phone_verified = True
                access_token = generate_access_token(user_obj)
                refresh_token = generate_refresh_token(user_obj)

                # response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
                # print(access_token)
                user_obj.save()
                if (user_obj.is_gender and user_obj.is_passion and user_obj.is_tall and user_obj.is_location and
                    user_obj.is_interest_in and user_obj.is_idealmatch and user_obj.is_marital_status and user_obj.is_media) == True:
                    is_complete_profile = True
                else:
                    is_complete_profile = False

                return Response(
                    {'success': True, 'message': 'your OTP is verified', 'status': 200, 'is_register': True,"token":access_token
                      ,"user": {
                        'id': user_obj.id,
                        'email': user_obj.email,
                        'mobile': user_obj.mobile,
                        'country_code': user_obj.country_code,
                        'name': user_obj.name,
                        "is_complete_profile": is_complete_profile,
                        'is_verified': user_obj.is_verified, }

                     },
                    status=status.HTTP_200_OK)
            return Response({'success': "success", 'message': 'Wrong OTP', "status": 403, "data": serializers.data},
                            status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            print(e)
        return Response(
            {'success': False, 'message': ' Mobile Number Not Registered', 'status': 404, 'is_register': False},
            status=status.HTTP_404_NOT_FOUND)


class GetUserDetailV2(GenericAPIView):

    """
    Retrieve, Checklist Api.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerializer
    # permission_classes = [IsAuthenticated,]

    # def get_object(self, user_id):
    #     try:
    #         return User.objects.get(id=user_id)
    #     except User.DoesNotExist:
    #         raise Http404

    @swagger_auto_schema(

        operation_summary=" Get User Detail",

        tags=['Account']
    )
    def get(self, request,  format=None):

        # adduserdetail = self.get_object(user_id)
        req = request.user
        # print (req)
        serializer = UserDetailSerializer(req)
        return Response({"success": True, "status": 200, "data": serializer.data }, status=status.HTTP_200_OK)


from django.contrib.auth import logout
class LogoutApiView(APIView):
    permission_class = (IsAuthenticated,)

    @swagger_auto_schema(

        operation_summary=" Api for User Logout ",

        tags=['Account']
    )
    def get(self, request, format=None):
        # simply delete the token to force a login
        # print(request.user.auth_token.delete())
        logout(request)
        return Response({'message': "Successfully LogOut",'status':200 ,'success': True},status=status.HTTP_200_OK)



class UserVerifiedAPI(GenericAPIView):

    """
    Retrieve, Checklist Api.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserVerifiedSerilaizer
    # permission_classes = [IsAuthenticated,]

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(

        operation_summary=" Api for User Verified ",

        tags=['Account']
    )
    def get(self, request,  user_id,format=None):

        adduserdetail = self.get_object(user_id)
        # req = request.user
        # print (req)
        serializer = UserVerifiedSerilaizer(adduserdetail)
        return Response({"success": True, "status": 200, "data": serializer.data }, status=status.HTTP_200_OK)


from usermedia.models import *
from usermedia.serializers import *

class UserEditProfileMediaAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        # user_id = self.kwargs.get('user_id')
        user_data = get_object_or_404(User, id=user_id)
        user_edit_data = MediaPost.objects.filter(user_id=user_id)
        # print (len(user_edit_data))
        # user_data = User.objects.filter(id=user_id)
        serializer = UserSerializer(user_data,)
        user_edit = UserMediaEditSerializer(user_edit_data , many=True)
        # if serializer.is_valid():
        #     user_data = serializer.save()
        return Response({"message": "User Profile is Successfully Updated!", "status": 200, "success": True,
                             "data": serializer.data,'media' : user_edit.data}, status= status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(

        operation_summary="User Update Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'passion': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Passion'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Gender'),
                'idealmatch': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Idealmatch'),
                'marital_status': openapi.Schema(type=openapi.TYPE_STRING, description='Add User marital_status'),
                'tall': openapi.Schema(type=openapi.TYPE_STRING, description='Add User tall'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='Add User location'),
                'interest_in': openapi.Schema(type=openapi.TYPE_STRING, description='Add User interest_in'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Add User email'),

            }),

        tags=['Account']
    )


    def put(self, request, *args, **kwargs):

        user_id = request.user.id
        # user_id = self.kwargs.get('user_id')
        user_data = get_object_or_404(User, id=user_id)
        user_edit_data = MediaPost.objects.filter(user_id=user_id).select_related("user")
        # serializer = UserSerializer(user_edit_data, data=request.data)
        serializer = UserMediaEditSerializer(user_edit_data, data=request.data)

        if serializer.is_valid():
            user_edit_data = serializer.save()

            return Response({"message": "User Profile is Successfully Updated!", "status": 200, "success": True,
                             "data": UserSerializer(user_edit_data).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)