from uuid import UUID

# Create your views here.
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.viewsets import *
from .models import *
from .serializers import *
from rest_framework.parsers import *
from rest_framework.permissions import *
from account.models import *
from . models import *


class UserMediaAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetMediaPostSerializers
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
      
        operation_summary = "User Media By User Id",

        tags = ['User Media']
    )
    def get(self, request, user_id, *args, **kwargs):
        user = MediaPost.objects.filter(user_id=user_id)
        serializer = GetMediaPostSerializers(user,context={'request': request}, many=True)
        return Response({"media": serializer.data ,"status":200 ,"success": True}, status=status.HTTP_200_OK)


class UserMediaAPIPost(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MediaPostSerializers
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
    def get(self, request, *args, **kwargs):
        media = MediaPost.objects.all()
        serializer = MediaPostSerializers(media,context={'request': request}, many=True)
        return Response({"success": True, "status":200 , "post": serializer.data},status=status.HTTP_200_OK)

class GetMediaUploadApi(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetMediaPostSerializers
    @swagger_auto_schema(
      
        operation_summary = "Get User Media By Media Id  ",
    
        tags = ['User Media']
    )
    
    def get(self, request, id, *args, **kwargs):
        posts = MediaPost.objects.filter(id=id)
        serializer = MediaPostSerializers(posts, many=True)
        return Response({"status":200 ,"success":True, "post": serializer.data}, status=status.HTTP_200_OK)

class MediaUploadApi(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MediaPostSerializers
    # def get(self, request, *args, **kwargs):
    #     posts = MediaPost.objects.all()
    #     serializer = MediaPostSerializers(posts, many=True)
    #     return Response({"status":200 ,"success":True, "post": serializer.data}, status=status.HTTP_200_OK)

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

        operation_summary = "Create User Media Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'media': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Media Data'),

            'caption': openapi.Schema(type=openapi.TYPE_STRING, description='Add Caption'),
            
        }),

        tags = ['User Media']
    )
    def post(self, request, *args, **kwargs):

        # user=request.user.id

        caption =request.data.get('caption'),
        media = request.data.get('media'),
        if media is not None:
            user= request.user.id
            obj = User.objects.filter(id=user)
            obj.update(is_media=True)
            string = request.data['media']
            name = string.split(',')

            for i in range(len(name)):
                aa = MediaPost.objects.create(user=request.user,media=name[i],caption=caption)

            # print (aa)

            # if serializer.is_valid():
            #
            #     # serializer.save()
            #     # serializers = serializer.data['media']

            return Response({"success": True, "message": "User Media Added!","status": 201,"post": "post"}, status=status.HTTP_201_CREATED)
        return Response({"status": 400 ,"message": False}, status=status.HTTP_400_BAD_REQUEST)


class MediaReactionApi(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MediaPostSerializers

    def get(self, request):
        userView = MediaView.objects.all()
        userLike = MediaLike.objects.all()
        userShare = MediaShare.objects.all()
        serializerView = MediaViewSerializers(userView, many=True)
        serializerLike = MediaLikeSerializers(userLike, many=True)
        serializerShare = MediaShareSerializers(userShare, many=True)
        return Response({"success": True, "status":200 ,"data View": serializerView.data, "data Like": serializerLike.data,
                         "data share": serializerShare.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(

        operation_summary="Create User Media  Add Reaction Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'media': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Media Data'),

                'user': openapi.Schema(type=openapi.TYPE_STRING, description='user id '),
                'flag': openapi.Schema(type=openapi.TYPE_STRING, description='add flag 1  for  view  , 2 for  like'),

            }),

        tags=['User Media']
    )

    def post(self, request, format='json'):
        data = {
            'user': request.data['user'],
            'media': request.data['media']
        }
        user = request.data['user']
        media = request.data['media']
        postdata = int(media)
        flag = request.data['flag']
        flagdata = int(flag)
        obj = MediaPost.objects.filter(id=postdata)
        serializerView = MediaViewSerializers(data=request.data)
        serializerLike = MediaLikeSerializers(data=request.data)
        serializerShare = MediaShareSerializers(data=request.data)
        if serializerView.is_valid():
            if flagdata == 1:
                if MediaView.objects.filter(user=user,media=postdata).exists():
                    return Response(
                        {"message": "User Already Post Viewed", "success": "False", "data": serializerView.data},
                        status=status.HTTP_201_CREATED)

                else:
                    obj = obj[0]
                    obj.view_count = obj.view_count + 1
                    obj.save(update_fields=("view_count",))
                    serializerView.save()

                    return Response(

                        {"message": "User Post View Successfully", "status":200 ,"success": "True", "data": serializerView.data},
                        status=status.HTTP_201_CREATED)
        if serializerLike.is_valid():
            if flagdata == 2:
                if MediaLike.objects.filter(user=user,media=postdata).exists():
                    return Response(
                        {"message": "User Already Post Liked", "success": "False", "data": serializerLike.data},
                        status=status.HTTP_201_CREATED)
                else:
                    obj = obj[0]
                    obj.like_count = obj.like_count + 1
                    obj.save(update_fields=("like_count",))
                    serializerLike.save()

                    return Response(
                        {"message": "User Post Like Successfully", "success": "True", "data": serializerLike.data},
                        status=status.HTTP_201_CREATED)
        if serializerShare.is_valid():
            if flagdata == 3:
                obj = obj[0]
                obj.share_count = obj.share_count + 1
                obj.save(update_fields=("share_count",))
                serializerShare.save()

                return Response(
                    {"message": "User Post Shared Successfully", "status" :201,"success": "True", "data": serializerShare.data},
                    status=status.HTTP_201_CREATED)
        # if serializerLike.is_valid():
        #     try:
        #         if flagdata == 4:
        #             obj = obj[0]
        #             obj.is_like = obj.is_like - 1
        #             obj.save(update_fields=("is_like",))
        #             serializerLike.save()
        #
        #             return Response(
        #                 {"message": "User Post Dislike Successfully", "success": "True", "data": serializerLike.data},
        #                 status=status.HTTP_201_CREATED)
        #     except Exception as e:
        #         print(e)
        #         return Response({"message": "User Post Already Disliked", "success": "False", "data": serializerLike.data},
        #                         status=status.HTTP_201_CREATED)

        else:
            return Response({"message": "Data Not Valid","status" : 400, "success": "error", "flag": False},
                            status=status.HTTP_400_BAD_REQUEST)
            # return Response({"success": "error", "data": serializerLike.errors}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"success": "error", "data": serializerShare.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Bad Request", "status": 400,"success": "error"},
                        status=status.HTTP_400_BAD_REQUEST)


class MediaViewAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MediaPostSerializers
    def get(self, request, id, *args, **kwargs):
        media = MediaView.objects.filter(media_id=id)
        print(media)
        serializer = MediaViewSerializers(media, many=True)
        return Response({"success" : True,"status" : 200 ,"data":serializer.data}, status=status.HTTP_200_OK)


class MediaLikeAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MediaPostSerializers
    def get(self, request, id, *args, **kwargs):
        media = MediaLike.objects.filter(media_id=id)
        print(media)
        serializer = MediaLikeSerializers(media, many=True)
        return Response({"success" : True,"status" : 200 ,"data":serializer.data}, status=status.HTTP_200_OK)


class MediaShareAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MediaPostSerializers
    def get(self, request, id, *args, **kwargs):
        media = MediaShare.objects.filter(media_id=id)
        print(media)
        serializer = MediaShareSerializers(media, many=True)
        return Response({"success" : True,"status" :200 ,"data":serializer.data}, status=status.HTTP_200_OK)

# /Users/apple/Desktop/Dating-Backend

class UserMediaDeleteApi (GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self,media_id):

        try:
            # pk = request.user
            return MediaPost.objects.get(id=media_id)
        except MediaPost.DoesNotExist:
            raise Http404

    @swagger_auto_schema(

        operation_summary="User Media Delete Api",
        tags=['User Media']
    )

    def delete(self, request, media_id, format=None):

        media_view = self.get_object(media_id)
        opeartion = media_view.delete()
        data = {}
        if opeartion:
            data['success'] = "Successfully Deleted!"
            data['status'] = 204
        else :
            data["failed"] = "Failed Deleted!"
            data['status'] = 404
        return Response(data=data)