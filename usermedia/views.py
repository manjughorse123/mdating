from uuid import UUID

# Create your views here.
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


class UserMediaAPI(APIView):
    def get(self, request, id, *args, **kwargs):
        user = MediaPost.objects.filter(user_id=id)
        serializer = MediaPostSerializers(user, many=True)
        return Response({"media": serializer.data}, status=status.HTTP_200_OK)


class UserMediaAPIPost(APIView):
    def get(self, request, *args, **kwargs):
        media = MediaPost.objects.all()
        serializer = MediaPostSerializers(media, many=True)
        return Response({"success": "True", "post": [serializer.data]}, status=status.HTTP_200_OK)


class MediaUploadApi(APIView):
    def get(self, request, id, *args, **kwargs):
        posts = MediaPost.objects.filter(id=id)
        serializer = MediaPostSerializers(posts, many=True)
        return Response({"message": True, "post": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'caption': request.data.get('caption'),
            'media': request.data.get('media'),
            'user': request.data.get('user')

        }
        serializer = MediaPostSerializers(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": True, "post": [serializer.data]}, status=status.HTTP_201_CREATED)
        return Response({"message": False, "post": [serializer.errors]}, status=status.HTTP_400_BAD_REQUEST)


class MediaReactionApi(APIView):

    def get(self, request):
        userView = MediaView.objects.all()
        userLike = MediaLike.objects.all()
        userShare = MediaShare.objects.all()
        serializerView = MediaViewSerializers(userView, many=True)
        serializerLike = MediaLikeSerializers(userLike, many=True)
        serializerShare = MediaShareSerializers(userShare, many=True)
        return Response({"success": "True", "data View": serializerView.data, "data Like": serializerLike.data,
                         "data share": serializerShare.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        data = {
            'user': request.data.get('user'),
            'post': request.data.get('post')
        }
        user = request.POST.get('user')
        media = request.POST.get('media')
        postdata = int(media)
        flag = request.POST.get('flag')
        flagdata = int(flag)
        obj = MediaPost.objects.filter(id=postdata)
        serializerView = MediaViewSerializers(data=request.data)
        serializerLike = MediaLikeSerializers(data=request.data)
        serializerShare = MediaShareSerializers(data=request.data)
        if serializerView.is_valid():
            if flagdata == 1:
                if MediaView.objects.filter(user=user).exists():
                    return Response(
                        {"message": "User Already Post Viewed", "success": "False", "data": serializerView.data},
                        status=status.HTTP_201_CREATED)

                else:
                    obj = obj[0]
                    obj.is_view = obj.is_view + 1
                    obj.save(update_fields=("is_view",))
                    serializerView.save()

                    return Response(
                        {"message": "User Post View Successfully", "success": "True", "data": serializerView.data},
                        status=status.HTTP_201_CREATED)
        if serializerLike.is_valid():
            if flagdata == 2:
                if MediaLike.objects.filter(user=user).exists():
                    return Response(
                        {"message": "User Already Post Liked", "success": "False", "data": serializerLike.data},
                        status=status.HTTP_201_CREATED)
                else:
                    obj = obj[0]
                    obj.is_like = obj.is_like + 1
                    obj.save(update_fields=("is_like",))
                    serializerLike.save()

                    return Response(
                        {"message": "User Post Like Successfully", "success": "True", "data": serializerLike.data},
                        status=status.HTTP_201_CREATED)
        if serializerShare.is_valid():
            if flagdata == 3:
                obj = obj[0]
                obj.is_share = obj.is_share + 1
                obj.save(update_fields=("is_share",))
                serializerShare.save()

                return Response(
                    {"message": "User Post Shared Successfully", "success": "True", "data": serializerShare.data},
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
            return Response({"message": "Data Not Valid", "success": "error", "flag": False},
                            status=status.HTTP_400_BAD_REQUEST)
            # return Response({"success": "error", "data": serializerLike.errors}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"success": "error", "data": serializerShare.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Internal Server Error", "success": "error"},
                        status=status.HTTP_400_BAD_REQUEST)


class MediaViewAPI(APIView):
    def get(self, request, id, *args, **kwargs):
        media = MediaView.objects.filter(media_id=id)
        print(media)
        serializer = MediaViewSerializers(media, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaLikeAPI(APIView):
    def get(self, request, id, *args, **kwargs):
        media = MediaLike.objects.filter(media_id=id)
        print(media)
        serializer = MediaLikeSerializers(media, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaShareAPI(APIView):
    def get(self, request, id, *args, **kwargs):
        media = MediaShare.objects.filter(media_id=id)
        print(media)
        serializer = MediaShareSerializers(media, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# /Users/apple/Desktop/Dating-Backend
