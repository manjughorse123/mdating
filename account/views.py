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


class LoginAttempt(APIView):

    def post(self, request, *args, **kwargs):
        mobile = request.POST.get('mobile')
        country_code = request.POST.get('country_code')

        user = User.objects.filter(mobile=mobile, country_code=country_code).first()
        if user is None:
            return Response({"message": "Wrong OTP"}, status=status.HTTP_400_BAD_REQUEST)
        otp = str(random.randint(999, 9999))
        user.otp = otp
        user.save()
        send_otp(mobile, otp)
        request.sessions['mobile'] = mobile
        return Response({"message": "redirect to registrations pages"}, status=status.HTTP_400_BAD_REQUEST)


class LoginOtp(APIView):

    def post(self, request, *args, **kwargs):
        print(request.user)
        mobile = request.session['mobile']
        otp = request.POST.get("otp")
        profile = User.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            user = User.objects.get(id=profile.user.id)
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Wrong OTP"}, status=status.HTTP_201_CREATED)


class Registration(APIView):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        country_code = request.POST.get('country_code')
        birth_date = request.POST.get('birth_date')
        check_user = User.objects.filter(email=email, mobile=mobile).first()
        if check_user:
            return Response({"message": "User Already Exists"}, status=status.HTTP_400_BAD_REQUEST)
        otp = str(random.randint(999, 9999))
        user = User(email=email, name=name, birth_date=birth_date, mobile=mobile, otp=otp, country_code=country_code)
        user.save()
        # send_otp(mobile, otp)
        # request.session['mobile'] = mobile
        return Response({"message": "Redirect OTP pages"}, status=status.HTTP_201_CREATED)


class VirifyOtp(APIView):
    def post(self, request, *args, **kwargs):
        mobile = request.session['mobile']
        otp = request.POST.get('otp')
        profile = User.objects.filter(mobile=mobile).first()
        if otp == profile.otp:
            return Response({"message": "Redirect to Next Pages"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Wrong Otp"}, status=status.HTTP_400_BAD_REQUEST)
