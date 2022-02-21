from django.shortcuts import render
from rest_framework.generics import *
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from .serializers import FAQSerializer
from rest_framework.views import *
from friend.models import *
from rest_framework.viewsets import *

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




