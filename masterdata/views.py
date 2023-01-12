from django.shortcuts import render
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import *
from rest_framework.permissions import *
from rest_framework.viewsets import *
from rest_framework.generics import *
from ckeditor.fields import RichTextField
from account.models import *
from account.serializers import *
from DatingApp.baseurl import base_url
from .serializers import *
from friend.models import *
# Create your views here.


def index(request):
    

    return  render(request, 'data/index.html')


def termAndConditionView(request):
      

    return  render(request, 'data/term-condition.html')

def faqHtmlView(request):
      

    return  render(request, 'data/faq.html')

class FAQView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = FAQSerializer

    @swagger_auto_schema(

        operation_summary="Get Faq  Api",


        tags=['Master data']
    )
    def get(self, request):
        faq = FAQ.objects.all()
        serializer = FAQSerializer(faq, many=True)
        return Response({"success": True, "message": " FAQ Data!", "status": 200, "data": serializer.data},
                        status=status.HTTP_200_OK)

    # def post(self, request, format='json'):
    #     serializer = FAQSerializer(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()

    #         return Response({"success": True, "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({"success": "error", "status": 400, "data": serializer.errors},
    #                         status=status.HTTP_400_BAD_REQUEST)


class GetMasterData(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = GenderSerializer

    @swagger_auto_schema(
        operation_summary="Get Master Data Api",
        tags=['Master data']
    )
    def get(self, request):
        gender = Gender.objects.all()
        passion = Passion.objects.all()
        ideal_m = IdealMatch.objects.all()
        maritalstatus = MaritalStatus.objects.all()
        heigth = Heigth.objects.all()
        gen_serializer = GenderSerializer(gender, many=True)
        pan_serializer = PassionSerializer(passion, many=True)
        ideal_serializer = IdealMatchSerializer(ideal_m, many=True)
        marital_serializer = MaritalStatusSerializer(maritalstatus, many=True)
        tall_serializer = HeightSerializer(heigth, many=True)
        return Response({"success": True, "message": " Master Data Deatil!", "status": 200, "base_url": base_url,
                         "data": {'gender': gen_serializer.data,
                                  'passion': pan_serializer.data,
                                  'idealmatch': ideal_serializer.data,
                                  'marital_status': marital_serializer.data,
                                  'tall': tall_serializer.data,
                                  "public-privacy":base_url+"/api/get-public-privacy/",
                                  "term-condition": base_url+"/api/term-and-condition/",
                                  "faq":base_url+"/api/faq-detail/"

                                  }},
                        status=status.HTTP_200_OK)


class FAQViewV2(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = FAQSerializer

    @swagger_auto_schema(

        operation_summary="Get Faq  Api",

        tags=['Master data']
    )
    def get(self, request):
        faq = FAQ.objects.all()
        serializer = FAQSerializer(faq, many=True)
        return Response({"success": True, "message": " FAQ Data!", "status": 200, "data": serializer.data},
                        status=status.HTTP_200_OK)

    # def post(self, request, format='json'):
    #     serializer = FAQSerializer(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()

    #         return Response({"success": True, "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({"success": "error", "status": 400, "data": serializer.errors},
    #                         status=status.HTTP_400_BAD_REQUEST)


class GetMasterDataV2(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GenderSerializer

    @swagger_auto_schema(
        operation_summary="Get Master Data Api",
        tags=['Master data']
    )
    def get(self, request):
        gender = Gender.objects.all()
        passion = Passion.objects.all()
        ideal_m = IdealMatch.objects.all()
        maritalstatus = MaritalStatus.objects.all()
        heigth = Heigth.objects.all()
        gen_serializer = GenderSerializer(gender, many=True)
        pan_serializer = PassionSerializer(passion, many=True)
        ideal_serializer = IdealMatchSerializer(ideal_m, many=True)
        marital_serializer = MaritalStatusSerializer(maritalstatus, many=True)
        tall_serializer = HeightSerializer(heigth, many=True)
        return Response(
            {"success": True, "message": " Master Data Deatil!", "status": 200, "base_url": base_url,
             "data": {'gender': gen_serializer.data,
                      'passion': pan_serializer.data,
                      'idealmatch': ideal_serializer.data,
                      'marital_status': marital_serializer.data,
                      'tall': tall_serializer.data

                      }},
            status=status.HTTP_200_OK)

import datetime
from  datetime import timedelta

date = datetime.date.today()
class AddNotificationData(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = NotificationDataSerializer

    @swagger_auto_schema(

        operation_summary="Get Notification Api",

        tags=['Master data']
    )
    def get(self, request):
        today = date.today()
        seven_day_before = today - timedelta(days=7)
        faq = NotificationData.objects.filter(user=request.user.id,create_at__gte=seven_day_before).order_by("-id")
        serializer = NotificationDataSerializer(faq, many=True)
        return Response({"success": True, "base_url":base_url,"message": " Notification Data!", "status": 200, "data": serializer.data},
                        status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = NotificationDataSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({"success": True,  "status": 201,"message": " Notification Add Data",  "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message": " Notification Data Not Added" ,"status": 400, "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)




class TermAndConditionView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = PublicUrlSerializer

    @swagger_auto_schema(
        operation_summary="Get Master Data Api",
        tags=['Master data']
    )
    def get(self, request):
        trem = PublicUrl.objects.filter(name="Term and Condition")
        
        trem_serializer = PublicUrlSerializer(trem, many=True)
        
        return Response({"success": True, "message": "Term and Condition Detail", "status": 200, "base_url": base_url,
                         "data":trem_serializer.data,
                                  },
                        status=status.HTTP_200_OK)



class PrivacyPolicyView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = PublicUrlSerializer

    @swagger_auto_schema(
        operation_summary="Get Master Data Api",
        tags=['Master data']
    )
    def get(self, request):
        trem = PublicUrl.objects.filter(name__icontains="Privacy Policy")
        
        trem_serializer = PublicUrlSerializer(trem, many=True)
        
        return Response({"success": True, "message": "Privacy Policy Detail", "status": 200, "base_url": base_url,
                         "data":trem_serializer.data,
                                  },
                        status=status.HTTP_200_OK)