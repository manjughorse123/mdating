from django.shortcuts import render, get_object_or_404
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import *
import random
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from .filters import *

class AddPostUserUpdateView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =PostUserUpdate.objects.all()
        serializer = PostUserUpdateSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = PostUserUpdateSerializer(data=request.data)
        
        if serializer.is_valid():   
                
            serializer.save()
            
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PostUserReactSerializerView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =PostUserReact.objects.all()
        serializer = PostUserReactSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        
        serializer = PostUserReactSerializer(data=request.data)
        
        if serializer.is_valid():   
            obj = PostUserUpdate.objects.filter(id=1)
            obj = obj[0]
            obj.is_view = obj.is_view + 1
            obj.save(update_fields=("is_view", ))
            serializer.save()
            
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class AddMatchLikeUserProfileView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =UserMatchProfile.objects.all()
        serializer = UserMatchProfileSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserMatchProfileSerializer(data=request.data)
        
        if serializer.is_valid():   
                
            serializer.save()
            
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddLikeToLikeView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =UserToUserLike.objects.all()
        serializer = UserToUserLikeSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserToUserLikeSerializer(data=request.data)
        
        if serializer.is_valid():   
                
            serializer.save()
            
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

 
class  PostCountLikeView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =UserToUserUnLike.objects.all()
        serializer = UserToUserUnLikeSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserToUserUnLikeSerializer(data=request.data)
        
        if serializer.is_valid():  
            ab = serializer.validated_data['user']
            like_profile_user = serializer.validated_data['like_profile_user']
            if request.data['flag'] == '1':
                if UserToUserLike.objects.get(like_profile_user=like_profile_user):
                    return Response({"success": "error", "data": "user already like  another user "}, status=status.HTTP_400_BAD_REQUEST)
            else:
                obj = UserToUserLike.objects.get(user=ab)
                obj.is_like = True
                obj.save(update_fields=("is_like", ))
                
            if request.data['flag'] == '2':
                if UserToUserLike.objects.get(like_profile_user=like_profile_user):
                    
                    return Response({"success": "error", "data": "user already Dislike Another User "}, status=status.HTTP_400_BAD_REQUEST)
                else :    
                    obj = UserToUserLike.objects.get(user=ab)
                
                    obj.is_like = False
                    obj.save(update_fields=("is_like", ))
            if request.data['flag'] == '3':
          
                obj = UserToUserLike.objects.get(user=ab)
                obj =  obj.id 
                objs = UserToUserLike.objects.get(id=obj) 
                objs.delete()
        
            serializer.save()
            
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


