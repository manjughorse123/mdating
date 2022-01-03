from django.conf import settings
from django.contrib.auth import login
from rest_framework.generics import *
from .serializers import *
import random
import http.client
from rest_framework.views import *
from .models import *


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
                    {"message": "mobile no. not registered", "success": False},
                    status=status.HTTP_404_NOT_FOUND)
            otp = str(random.randint(999, 9999))
            user.otp = otp
            user.save()
            return Response({"message": "Done", "success": True,},
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
                return Response({"message": "mobile Already Exists", 'success': False}, status=status.HTTP_400_BAD_REQUEST)
            if check_email:
                return Response({"message": "email Already Exists", 'success': False}, status=status.HTTP_400_BAD_REQUEST)

            otp = str(random.randint(999, 9999))
            user = User(email=email, name=name, birth_date=birth_date, mobile=mobile, otp=otp,
                        country_code=country_code)
            user.save()

            return Response({"message": "Your Registrations is successfully", "success": True},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'success': False, 'message': 'internal server error'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OTPVerify(APIView):
    def post(self, request):
        try:
            mobile = request.POST.get("mobile")
            otp = request.POST.get("otp")
            user_obj = User.objects.get(mobile=mobile, otp=otp)

            if user_obj.otp == otp:
                user_obj.is_phone_verified = True
                user_obj.save()
                return Response({'success': True, 'message': 'your OTP is verified'}, status=status.HTTP_200_OK)
            return Response({'flag': success, 'message': 'Wrong OTP'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
        return Response({'success': False, 'message': 'internal server error'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserData(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
