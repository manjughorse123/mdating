from django.shortcuts import render
from rest_framework.generics import *
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from .serializers import FAQSerializer
from rest_framework.views import *
from friend.models import *
from rest_framework.viewsets import *
from account.models import *
from account.serializers import *

# Create your views here.
class FAQView(GenericAPIView):
    # permission_classes = (AllowAny,)
    serializer_class = FAQSerializer
    @swagger_auto_schema(
      
        operation_summary = "Get Faq  Api",
    

        tags = ['Master data']
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
    # permission_classes = (AllowAny,)
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
        return Response({"success": True, "message": " Master Data Deatil!", "status": 200,"base_url":"http://18.224.254.170",
                         "data": {'gender':gen_serializer.data,
                                  'passion':pan_serializer.data,
                                  'idealmatch': ideal_serializer.data,
                                  'marital_status': marital_serializer.data,
                                  'tall': tall_serializer.data

                                  }},
                        status=status.HTTP_200_OK)