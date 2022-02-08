from django.shortcuts import render, get_object_or_404
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import *
import random
from rest_framework import status
from rest_framework import viewsets


# Create your views here.
class UserVerificationView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        user_verify =UserVerification.objects.all()
        serializer = UserVerificationSerializer(user_verify, many=True)
        return Response({"success": True, "status": 200,"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserVerificationSerializer(data=request.data)
        
        if serializer.is_valid():   
                
            serializer.save()
            
            return Response({"success": True, "status": 201,"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class AdminUserVerifiedView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        admin_user_verify =AdminUserVerified.objects.all()
        serializer = AdminUserVerifiedSerializer(admin_user_verify, many=True)
        return Response({"success": True, "status": 200,"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = AdminUserVerifiedSerializer(data=request.data)
        
        if serializer.is_valid():   
                
            serializer.save()
            
            return Response({"success": True, "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error","status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
