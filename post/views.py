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


class PostUploadApi(GenericAPIView):
    serializer_class =  PostUploadSerializers
    def get(self, request, id, *args, **kwargs):
        posts = PostUpload.objects.filter(id=id)
        serializer = PostUploadSerializers(posts, many=True)
        return Response({"success": True,"status" : 200, "message" : "User Post by Post ID"  ,"data": serializer.data}, status=status.HTTP_200_OK)

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

            return Response({"message": True,"status":201, "post": [serializer.data]}, status=status.HTTP_201_CREATED)
        return Response({"message": False,"status":400, "post": [serializer.errors]}, status=status.HTTP_400_BAD_REQUEST)


class UserImages(GenericAPIView):
    serializer_class = PostUploadSerializers
    def get(self, request, id, *args, **kwargs):
        user = PostUpload.objects.filter(user_id=id)
        serializer = PostUploadSerializers(user, many=True)
        return Response({"success": True ,"post": serializer.data,"message" :"User Post by User ","status":200}, status=status.HTTP_200_OK)


class PostReactionApi(GenericAPIView):
    serializer_class = PostViewSerializers

    def get(self, request):
        userView = PostView.objects.all()
        userLike = PostLike.objects.all()
        userShare = PostShare.objects.all()
        serializerView = PostViewSerializers(userView, many=True)
        serializerLike = PostLikeSerializers(userLike, many=True)
        serializerShare = PostShareSerializers(userShare, many=True)
        return Response({"success": True, "status":200,"data View": serializerView.data,"data View count": len(serializerView.data), "data Like": serializerLike.data,
                        "message": "Post Reaction" ,"data share": serializerShare.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        data = {
            'user': request.data.get('user'),
            'post': request.data.get('post')
        }
        user = request.data.get('user')
        post = request.data.get('post')
        postdata = int(post)
        flag = request.data.get('flag')
        flagdata = int(flag)
        obj = PostUpload.objects.filter(id=postdata)
        serializerView = PostViewSerializers(data=request.data)
        serializerLike = PostLikeSerializers(data=request.data)
        serializerShare = PostShareSerializers(data=request.data)
        if serializerView.is_valid():
            if flagdata == 1:
                if PostView.objects.filter(user=user).exists():
                    return Response(
                        {"message": "User Already Post Viewed","status":400, "success": False, "user": [serializerView.data]},
                        status=status.HTTP_400_BAD_REQUEST)

                else:
                    obj = obj[0]
                    obj.is_view = obj.is_view + 1
                    obj.save(update_fields=("is_view",))
                    serializerView.save()

                    return Response(
                        {"message": "User Post View Successfully", "status":201,"success": True, "user": [serializerView.data]},
                        status=status.HTTP_201_CREATED)
        if serializerLike.is_valid():
            if flagdata == 2:
                if PostLike.objects.filter(user=user).exists():
                    return Response(
                        {"message": "User Already Post Liked","status":400, "success": False, "user": [serializerLike.data]},
                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = obj[0]
                    obj.is_like = obj.is_like + 1

                    obj.save(update_fields=("is_like",))
                    serializerLike.save()

                    return Response(
                        {"message": "User Post Like Successfully","status":201, "success": True, "user": [serializerLike.data]},
                        status=status.HTTP_201_CREATED)
        if serializerShare.is_valid():
            if flagdata == 3:
                obj = obj[0]
                obj.is_share = obj.is_share + 1
                obj.save(update_fields=("is_share",))
                serializerShare.save()

                return Response(
                    {"message": "User Post Shared Successfully","status":201, "success": True, "user": [serializerLike.data]},
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
            return Response({"success": "error", "user": [serializerLike.data]}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"success": "error", "data": serializerLike.errors}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"success": "error", "data": serializerShare.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Internal Server Error! or Not Valid Input !!", "success": False, "status": 400},
                        status=status.HTTP_400_BAD_REQUEST)

# class AllPostAPI(ListAPIView):
#     queryset = PostUpload.objects.all()
#     serializer_class = PostUploadSerializers


    

class GetPostViewdetailView(GenericAPIView):
    serializer_class = PostViewSerializers
    """
    Retrieve, update or delete  a media instance.
    """
    def get_object(self, pk):
        try:
            return PostView.objects.get(pk=pk)
        except PostView.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
    
        post_view = self.get_object(pk)
        serializer = PostViewSerializers(post_view)
        return Response({"success": True, "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

    
    def delete(self, request, pk, format=None):
        post_view = self.get_object(pk)
        post_view.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AllPostAPI(GenericAPIView):
    serializer_class = PostUploadSerializers
    def get(self, request, *args, **kwargs):
        post = PostUpload.objects.all()
        serializer = PostUploadSerializers(post, many=True)
        return Response({"success": True,"status":200 , "message" : "All Users Post!","post": serializer.data}, status=status.HTTP_200_OK)


class PostViewAPI(GenericAPIView):
    serializer_class  = PostViewSerializers

    def get(self, request, id, *args, **kwargs):
        post = PostView.objects.filter(post_id=id)
        serializer = PostViewSerializers(post, many=True)

        return Response({"success": True,"status":200, "user": [serializer.data]}, status=status.HTTP_200_OK)


class PostLikeAPI(GenericAPIView):
    serializer_class = PostLikeSerializers
    def get(self, request, id, *args, **kwargs):
        post = PostLike.objects.filter(post_id=id)
        serializer = PostLikeSerializers(post, many=True)
        return Response({"success": True,"status":200, "user": [serializer.data]}, status=status.HTTP_200_OK)


class PostShareAPI(GenericAPIView):
    serializer_class = PostShareSerializers
    def get(self, request, id, *args, **kwargs):
        post = PostShare.objects.filter(post_id=id)
        serializer = PostShareSerializers(post, many=True)
        return Response({"success": True, "status":200, "user": [serializer.data]}, status=status.HTTP_200_OK)

