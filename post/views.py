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


class PostUploadApi(APIView):
    def get(self, request, id, *args, **kwargs):
        posts = PostUpload.objects.filter(id=id)
        serializer = PostUploadSerializers(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'message': request.data.get('message'),
            'post': request.data.get('post'),
            'user': request.data.get('user')

        }
        serializer = PostUploadSerializers(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserImages(APIView):
    def get(self, request, id, *args, **kwargs):
        user = PostUpload.objects.filter(user_id=id)
        serializer = PostUploadSerializers(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMediaAPI(APIView):
    def get(self, request, id, *args, **kwargs):
        user = MediaPost.objects.filter(user_id=id)
        serializer = MediaPostSerializers(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMediaAPIPost(ListCreateAPIView):
    queryset = MediaPost.objects.all()
    serializer_class = MediaPostSerializers


class MediaReactionApi(APIView):

    def get(self, request):
        mediaReaction = MediaReaction.objects.all()
        serializer = MediaReactionSerializers(mediaReaction, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        data = {
            'user': request.data.get('user'),
            'media': request.data.get('media')
        }
        media = request.POST.get('media')
        postdata = int(media)
        flag = request.POST.get('flag')
        flagdata = int(flag)
        serializer = MediaReactionSerializers(data=request.data)
        if serializer.is_valid():
            obj = MediaPost.objects.filter(id=postdata)
            if flagdata == 1:
                obj = obj[0]
                obj.is_view = obj.is_view + 1
                obj.save(update_fields=("is_view",))
                serializer.save()

                return Response({"message": "User Media View Successfully", "success": "True", "data": serializer.data},
                                status=status.HTTP_201_CREATED)
            if flagdata == 2:
                obj = obj[0]
                obj.is_like = obj.is_like + 1
                obj.save(update_fields=("is_like",))
                serializer.save()

                return Response({"message": "User Media Like Successfully", "success": "True", "data": serializer.data},
                                status=status.HTTP_201_CREATED)

            if flagdata == 3:
                obj = obj[0]
                obj.is_share = obj.is_share + 1
                obj.save(update_fields=("is_share",))
                serializer.save()

                return Response(
                    {"message": "User Media Shared Successfully", "success": "True", "data": serializer.data},
                    status=status.HTTP_201_CREATED)
            try:
                if flagdata == 4:
                    obj = obj[0]
                    obj.is_like = obj.is_like - 1
                    obj.save(update_fields=("is_like",))
                    serializer.save()

                    return Response(
                        {"message": "User Media Dislike Successfully", "success": "True", "data": serializer.data},
                        status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response({"message": "User Media Already Disliked", "success": "False", "data": serializer.data},
                                status=status.HTTP_201_CREATED)

        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PostReactionApi(APIView):

    def get(self, request):
        userReaction = PostReaction.objects.all()
        serializer = PostReactionSerializers(userReaction, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        data = {
            'user': request.data.get('user'),
            'post': request.data.get('post')
        }
        post = request.POST.get('post')
        postdata = int(post)
        flag = request.POST.get('flag')
        flagdata = int(flag)
        serializer = PostReactionSerializers(data=request.data)
        if serializer.is_valid():
            obj = PostUpload.objects.filter(id=postdata)
            if flagdata == 1:
                obj = obj[0]
                obj.is_view = obj.is_view + 1
                obj.save(update_fields=("is_view",))
                serializer.save()

                return Response({"message": "User Post View Successfully", "success": "True", "data": serializer.data},
                                status=status.HTTP_201_CREATED)
            if flagdata == 2:
                obj = obj[0]
                obj.is_like = obj.is_like + 1
                obj.save(update_fields=("is_like",))
                serializer.save()

                return Response({"message": "User Post Like Successfully", "success": "True", "data": serializer.data},
                                status=status.HTTP_201_CREATED)

            if flagdata == 3:
                obj = obj[0]
                obj.is_share = obj.is_share + 1
                obj.save(update_fields=("is_share",))
                serializer.save()

                return Response(
                    {"message": "User Post Shared Successfully", "success": "True", "data": serializer.data},
                    status=status.HTTP_201_CREATED)
            try:
                if flagdata == 4:
                    obj = obj[0]
                    obj.is_like = obj.is_like - 1
                    obj.save(update_fields=("is_like",))
                    serializer.save()

                    return Response(
                        {"message": "User Post Dislike Successfully", "success": "True", "data": serializer.data},
                        status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response({"message": "User Post Already Disliked", "success": "False", "data": serializer.data},
                                status=status.HTTP_201_CREATED)

        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AllPostAPI(ListAPIView):
    queryset = PostUpload.objects.all()
    serializer_class = PostUploadSerializers
