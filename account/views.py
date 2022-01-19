from django.conf import settings
from rest_framework.generics import *
from .serializers import *
import random
import http.client
from rest_framework.views import *
from .models import *
from rest_framework_jwt.settings import api_settings
from rest_framework.viewsets import *


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
            otp = str(1234)
            user.otp = otp
            user.save()
            return Response({"message": "Done", "success": True, 'is_register': True},
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
                return Response({"message": "mobile Already Exists", 'success': False, 'is_register': False},
                                status=status.HTTP_400_BAD_REQUEST)
            if check_email:
                return Response({"message": "email Already Exists", 'success': False, 'is_register': False},
                                status=status.HTTP_400_BAD_REQUEST)

            # otp = str(random.randint(999, 9999))
            otp = str(1234)
            user = User(email=email, name=name, birth_date=birth_date, mobile=mobile, otp=otp,
                        country_code=country_code)
            print(type(user))
            user.save()
            return Response({"message": "Your Registrations is successfully", "success": True, 'is_register': True,
                            },
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
                return Response({"message": "User Already Exists with  This Email! "}, status=status.HTTP_400_BAD_REQUEST)
            if check_mobile:
                return Response({"message": "User Already Exists with This Phone NO!"}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            data = serializer.data
            if user:
                return Response({'data': data,
                                 "status": status.HTTP_201_CREATED,
                                 "msg":  msg})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerify(APIView):
    def post(self, request):
        # try:
        mobile = request.POST.get("mobile")
        otp = request.POST.get("otp")
        country_code = request.POST.get("country_code")
        user_obj = User.objects.get(mobile=mobile, otp=otp, country_code=country_code)
        if user_obj.otp == otp:
            user_obj.is_phone_verified = True

            user_obj.save()
            return Response(
                {'success': True, 'message': 'your OTP is verified', 'is_register': True,
                 'id': user_obj.id,
                 'email': user_obj.email,
                 'mobile': user_obj.mobile,
                 'country_code': user_obj.country_code,
                 'name': user_obj.name,
                 'bio': user_obj.bio,
                 'birth_date':user_obj.birth_date,
                 'otp':user_obj.otp,
                 'relationship_status':user_obj.relationship_status,
                 'education':user_obj.education,
                 'body_type':user_obj.body_type,
                 'gender':user_obj.gender,
                 # 'image':user_obj.image,
                 # 'userIntrest':user_obj.userinterest,
                 # 'idealmatch':user_obj.idealmatch,
                 'height':user_obj.height,
                 'location':user_obj.location,
                 'citylat':user_obj.citylat,
                 'citylong':user_obj.citylong,
                 'address':user_obj.address,
                 'city':user_obj.city,
                 'is_premium':user_obj.is_premium,
                 'is_verified':user_obj.is_verified,
                 'first_count':user_obj.first_count

                 },
                status=status.HTTP_200_OK)
        return Response({'success': "success", 'message': 'Wrong OTP'}, status=status.HTTP_403_FORBIDDEN)

        # except Exception as e:
        #     print(e)
        # return Response({'success': False, 'message': 'internal server error', 'is_register': False},
        #                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserData(ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # print(authentication_classes)
    # permission_classes = [IsAuthenticated]
    # print(permission_classes)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdate(RetrieveUpdateDestroyAPIView):
    # authentication_classes = [JWTAuthentication]
    # print(authentication_classes)
    # permission_classes = [IsAuthenticated]
    # print(permission_classes)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AddInterestView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        interest =Interest.objects.all()
        serializer = InterestSerializer(interest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        
        serializer = InterestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AddInterestdetailView(APIView):
    """
    Retrieve, update or delete  a Interest instance.
    """
    def get_object(self, pk):
        try:
            return Interest.objects.get(pk=pk)
        except Interest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        addInterest = self.get_object(pk)
        serializer = InterestSerializer(addInterest)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        addInterest = self.get_object(pk)
        serializer = InterestSerializer(addInterest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        addInterest = self.get_object(pk)
        serializer = InterestSerializer(
            addInterest,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        addInterest = self.get_object(pk)
        addInterest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddGenderView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        gender =Gender.objects.all()
        serializer = GenderSerializer(gender, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        
        serializer = GenderSerializer(data=request.data)
        
        if serializer.is_valid():
            gender = serializer.validated_data['gender']
            check_gender = Gender.objects.filter(gender=gender).first()
            
            if check_gender:
                return Response({"message": "gender Already Exists with  This name! "}, status=status.HTTP_400_BAD_REQUEST)
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
        serializer = GenderSerializer(addGender, data=request.data,partial=True)
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
        userMedia =UserMedia.objects.all()
        serializer = UserMediaSerializer(userMedia, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        
        serializer =UserMediaSerializer(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data['name']
            check_name = UserMedia.objects.filter(name=name).first()
            
            if check_name:
                return Response({"message": "media Already Exists with  This name! "}, status=status.HTTP_400_BAD_REQUEST)
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

    def put(self, request, pk, format=None):
        addUserMedia = self.get_object(pk)
        serializer = UserMediaSerializer(addUserMedia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        addUserMedia = self.get_object(pk)
        serializer = UserMediaSerializer(addUserMedia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        addUserMedia = self.get_object(pk)
        addUserMedia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddMaritalStatusView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        meritalstatus =MaritalStatus.objects.all()
        serializer = MaritalStatusSerializer(meritalstatus, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        
        serializer = MaritalStatusSerializer(data=request.data)
        
        if serializer.is_valid():
            m_status = serializer.validated_data['status']
            check_status = MaritalStatus.objects.filter(status=m_status).first()
            
            if check_status:
                return Response({"message": "media Already Exists with  This name! "}, status=status.HTTP_400_BAD_REQUEST)
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
        idealMatch =IdealMatch.objects.all()
        serializer = IdealMatchSerializer(idealMatch, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = IdealMatchSerializer(data=request.data)
        
        if serializer.is_valid():
            idealmatch = serializer.validated_data['idealmatch']
            check_name =IdealMatch.objects.filter(idealmatch=idealmatch).first()
            
            if check_name:
                return Response({"message": "idealmatch Already Exists with  This name! "}, status=status.HTTP_400_BAD_REQUEST)
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
        idealMatch =User.objects.all()
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
        useridealMatch =UserIdealMatch.objects.all()
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
class AddUserInterestView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =UserInterest.objects.all()
        serializer = UserInterestSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserInterestSerializer(data=request.data)
        
        if serializer.is_valid():        
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AddUserInterestdetailView(APIView):
    """
    Retrieve, update or delete  a media instance.
    """
    def get_object(self, pk):
        try:
            return UserInterest.objects.get(pk=pk)
        except UserInterest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
    
        adduserInterest = self.get_object(pk)
        serializer = UserInterestSerializer(adduserInterest)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        adduserInterest = self.get_object(pk)
        serializer = UserInterestSerializer(adduserInterest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        adduserInterest = self.get_object(pk)
        serializer = UserInterestSerializer(adduserInterest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        adduserInterest = self.get_object(pk)
        adduserInterest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class AddUserInterestView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =UserInterest.objects.all()
        serializer = UserInterestSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
    
        serializer = UserInterestSerializer(data=request.data)
        
        if serializer.is_valid():        
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class MatchProfileView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        
        # if in
        lista = []
        data1 ={}
        if UserInterest.objects.filter(interest=3):
            
            user_ideal =  UserInterest.objects.filter(interest=3)
            print ("datasdd",user_ideal)
        
        
        if UserInterest.objects.filter(interest=5):
            user_ideal1 =  UserInterest.objects.filter(interest=5)
            print ("data",user_ideal1)

        if UserIdealMatch.objects.filter(idealmatch=2):
            user_ideal =  UserIdealMatch.objects.filter(idealmatch=2)
            print ("datdadada",user_ideal)

        return Response({"success": "True"}, status=status.HTTP_200_OK)

   

class ProfileCountView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, pk ,request):
        user = User.objects.filter(pk = pk)
        # user.update(viewcount)

        return Response({"success": "True"}, status=status.HTTP_200_OK)



# class FriendRequestSend(APIView):





#     @login_required
# def friendship_add_friend(
#     request, to_username, template_name="friendship/friend/add.html"
# ):
#     """ Create a FriendshipRequest """
#     ctx = {"to_username": to_username}

#     if request.method == "POST":
#         to_user = user_model.objects.get(username=to_username)
#         from_user = request.user
#         try:
#             Friend.objects.add_friend(from_user, to_user)
#         except AlreadyExistsError as e:
#             ctx["errors"] = ["%s" % e]
#         else:
#             return redirect("friendship_request_list")

#     return render(request, template_name, ctx)
