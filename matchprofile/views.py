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
        userInterest = PostUserUpdate.objects.all()
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
        userInterest = PostUserReact.objects.all()
        serializer = PostUserReactSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):

        serializer = PostUserReactSerializer(data=request.data)

        if serializer.is_valid():
            obj = PostUserUpdate.objects.filter(id=1)
            obj = obj[0]
            obj.is_view = obj.is_view + 1
            obj.save(update_fields=("is_view",))
            serializer.save()

            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AddMatchLikeUserProfileView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =UserMatchProfile.objects.all()
        serializer = UserMatchProfileSerializer(userInterest, many=True)
        return Response({"success": True, "status": 200,"message": "Match Profile Data","data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserMatchProfileSerializer(data=request.data)
        if serializer.is_valid():   

            serializer.save()
            
            return Response({"success": True,"status": 201,"message": "User Match Profile Created!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "status": 400,"message": "Match Profile Data Not Found","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddLikeToLikeView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =UserToUserLike.objects.all()
        serializer = UserToUserLikeSerializer(userInterest, many=True)
        return Response({"success": True, "status": 200,"message": "User Profile Liked!","data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserToUserLikeSerializer(data=request.data)
        
        if serializer.is_valid():   
                
            serializer.save()
            
            return Response({"success": True,"status": 201,"message": "Liked User Profile", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

 
class  PostCountLikeView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =UserToUserUnLike.objects.all()
        serializer = UserToUserUnLikeSerializer(userInterest, many=True)
        return Response({"success": True, "status": 200,"message": "Match Profile Data Count","data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserToUserUnLikeSerializer(data=request.data)
        
        if serializer.is_valid():  
            ab = serializer.validated_data['user']
            like_profile_user = serializer.validated_data['like_profile_user']
            if request.data['flag'] == '1':
                if UserToUserLike.objects.get(like_profile_user=like_profile_user):
                    return Response({"success": "error","status": 400,"message":  "User Already like Profile "}, status=status.HTTP_400_BAD_REQUEST)
            else:
                obj = UserToUserLike.objects.get(user=ab)
                obj.is_like = True
                obj.save(update_fields=("is_like", ))
                
            if request.data['flag'] == '2':
                if UserToUserLike.objects.get(like_profile_user=like_profile_user):
                    
                    return Response({"success": "error","status": 400,"message":  "User Already Dislike Profile "}, status=status.HTTP_400_BAD_REQUEST)
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
            
            return Response({"success": True,"status": 201,"message": "Match Profile Data", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class MatchedUserProfileView(GenericAPIView):
    serializer_class = GetUserMatchProfileSerializer
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest = UserMatchProfile.objects.all()
        serializer = GetUserMatchProfileSerializer(userInterest, many=True)
        return Response(
            {"success": True, "status": 200, "message": "Match Profile Users All Data", "data": serializer.data},
            status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserMatchProfileSerializer(data=request.data)

        if serializer.is_valid():
            ab = serializer.validated_data['user']
            like_profile_user = serializer.validated_data['like_profile_user']
            if request.data['flag'] == '1':
                if UserMatchProfile.objects.filter(like_profile_user=like_profile_user):
                    return Response({"success": "error", "status": 400, "message": "User Already like Profile "},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = UserMatchProfile.objects.create(user = ab,like_profile_user=like_profile_user,is_like = True)

            if request.data['flag'] == '2':
                if UserMatchProfile.objects.filter(like_profile_user=like_profile_user,is_like =False):

                    return Response({"success": "error", "status": 400, "message": "User Already Dislike Profile "},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = UserMatchProfile.objects.filter(user=ab)

                    obj.is_like = False
                    # obj.save(update_fields=("is_like",))
                    obj.update()

            if request.data['flag'] == '3':
                obj = UserMatchProfile.objects.filter(like_profile_user=like_profile_user)
                obj = obj[0].id
                objs = UserMatchProfile.objects.filter(id=obj)
                objs.delete()
                return Response({"success": True,"message": "User Dislike !" ,"status": 200},status=status.HTTP_200_OK)

            # serializer.save()

            return Response({"success": True, "status": 201, "message": "Match Profile Data", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "status": 400, "data": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

