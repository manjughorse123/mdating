from django.db.models import Q
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.viewsets import *
from rest_framework.parsers import *
from rest_framework.permissions import *
from .models import *
from .serializers import *
from friend.models import *


class GetPostUploadApi(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class =  PostUploadSerializers
    @swagger_auto_schema(
      
        operation_summary = "Get All Post by Post id",
        tags = ['Post']
    )
    def get(self, request, post_id, *args, **kwargs):
        posts = PostUpload.objects.filter(id=post_id)
        serializer = PostUploadSerializers(posts, many=True)
        return Response({"success": True,"status" : 200, "message" : "User Post by Post ID"  ,"data": serializer.data}, status=status.HTTP_200_OK)


class PostUploadApi(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class =  PostUploadSerializers
    @swagger_auto_schema(
      
        operation_summary = "Create Post Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'post': openapi.Schema(type=openapi.TYPE_STRING, description='Add Post Data'),
            'user': openapi.Schema(type=openapi.TYPE_STRING, description='User Id'),
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Add Title'),
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Add Message'),
        }),

        tags = ['Post']
    )
    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'message': request.data.get('message'),
            'post': request.data.get('post'),
            # 'user': request.data.get('user')
            'user' : request.user.id

        }
        serializer = PostUploadSerializers(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": True,"status":201, "post": [serializer.data]}, status=status.HTTP_201_CREATED)
        return Response({"message": False,"status":400, "post": [serializer.errors]}, status=status.HTTP_400_BAD_REQUEST)


class UserImages(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostUploadSerializers

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
      
        operation_summary = "Get User Post by User Id  Api ",
        tags = ['Post']
    )
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user = PostUpload.objects.filter(user_id=user_id)
        # following_ids = request.user.following.values_list('id', flat=True)
        following_ids  =  FollowRequest.objects.filter(user_id=user_id)
        friends_ids = FriendList.objects.filter(user_id=user_id)
        following_id_list = []
        friend_id_list = []

        for i in range(len(following_ids)):

            following_id_data = following_ids[i].follow
            following_id_list.append(following_id_data)

        for fri in range(len(friends_ids)):
            friend_id_data = friends_ids[fri].friends
            friend_id_list.append(friend_id_data)

        posts_list = PostUpload.objects.filter(
            Q(user_id__in=following_id_list) | Q(user=user_id) | Q(user_id__in=friend_id_list)).order_by('-create_at').distinct()

        follow_serializer = PostUploadSerializers(posts_list,context={'request': request},many=True)

        return Response({"success": True ,'post': follow_serializer.data,"message" :"User Post by User ","status":200}, status=status.HTTP_200_OK)


class PostReactionApi(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostViewSerializers
    # @swagger_auto_schema(
    #
    #     operation_summary = "Get Post Reaction Api",
    #
    #     tags = ['Post']
    # )
    #
    # def get(self, request):
    #     userView = PostView.objects.all()
    #     userLike = PostLike.objects.all()
    #     userShare = PostShare.objects.all()
    #     serializerView = PostViewSerializers(userView, many=True)
    #     serializerLike = PostLikeSerializers(userLike, many=True)
    #     serializerShare = PostShareSerializers(userShare, many=True)
    #     return Response({"success": True, "status":200,"data View": serializerView.data,"data View count": len(serializerView.data), "data Like": serializerLike.data,
    #                     "message": "Post Reaction" ,"data share": serializerShare.data}, status=status.HTTP_200_OK)
    @swagger_auto_schema(
      
        operation_summary = "Create Post Reaction Api",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'post': openapi.Schema(type=openapi.TYPE_STRING, description='Add Post Data'),
            'user': openapi.Schema(type=openapi.TYPE_STRING, description='User Id'),
            'flag': openapi.Schema(type=openapi.TYPE_STRING, description='Add flag  1 for view and 2 for like'),

        }),

        tags = ['Post']
    )

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
                if PostView.objects.filter(user=user,post=post).exists():
                    return Response(
                        {"message": "User Already Post Viewed","status":400, "success": False, "user": [serializerView.data]},
                        status=status.HTTP_400_BAD_REQUEST)

                else:
                    obj = obj[0]
                    obj.is_view_count = obj.is_view_count + 1
                    obj.save(update_fields=("is_view_count",))
                    serializerView.save()

                    return Response(
                        {"message": "User Post View Successfully", "status":201,"success": True, "user": [serializerView.data]},
                        status=status.HTTP_201_CREATED)
        if serializerLike.is_valid():
            if flagdata == 2:
                if PostLike.objects.filter(user=user,post=post).exists():
                    return Response(
                        {"message": "User Already Post Liked","status":400, "success": False, "user": [serializerLike.data]},
                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = obj[0]
                    obj.is_like_count = obj.is_like_count + 1
                    obj.save(update_fields=("is_like_count",))
                    serializerLike.save()

                    return Response(
                        {"message": "User Post Like Successfully","status":201, "success": True, "user": [serializerLike.data]},
                        status=status.HTTP_201_CREATED)
        if serializerShare.is_valid():
            if flagdata == 3:
                obj = obj[0]
                obj.is_share_count = obj.is_share_count + 1
                obj.save(update_fields=("is_share_count",))
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
        #


        #         return Response({"message": "User Post Already Disliked", "success": "False", "data": serializerLike.data},
        #                         status=status.HTTP_201_CREATED)

        else:
            return Response({"success": "error", "user": [serializerLike.data]}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"success": "error", "data": serializerLike.errors}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"success": "error", "data": serializerShare.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": " Not Valid Input !!", "success": False, "status": 400},
                        status=status.HTTP_400_BAD_REQUEST)

# class AllPostAPI(ListAPIView):
#     queryset = PostUpload.objects.all()
#     serializer_class = PostUploadSerializers




class GetPostViewdetailView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostViewSerializers
    """
    Retrieve, update or delete  a media instance.
    """

    
    def get_object(self, pk):
        try:
            return PostView.objects.get(pk=pk)
        except PostView.DoesNotExist:
            raise Http404
    @swagger_auto_schema(
      
        operation_summary = "Get Post  View Detail Api",

        tags = ['Post']
    )

    def get(self, request, pk, format=None):
    
        post_view = self.get_object(pk)
        serializer = PostViewSerializers(post_view)
        return Response({"success": True, "status":200,"data": serializer.data}, status=status.HTTP_200_OK)

    
    # def delete(self, request, pk, format=None):
    #     post_view = self.get_object(pk)
    #     post_view.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class AllPostAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = PostUploadSerializers
    @swagger_auto_schema(
      
        operation_summary = "Get All User Post",

        tags = ['Post']
    )
    def get(self, request, *args, **kwargs):
        post = PostUpload.objects.all()
        serializer = PostUploadSerializers(post, many=True)
        return Response({"success": True,"status":200 , "message" : "All Users Post!","post": serializer.data}, status=status.HTTP_200_OK)


class PostViewAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class  = PostViewSerializers

    def get(self, request, id, *args, **kwargs):
        post = PostView.objects.filter(post_id=id)
        serializer = PostViewSerializers(post, many=True)

        return Response({"success": True,"status":200, "user": [serializer.data]}, status=status.HTTP_200_OK)


class PostLikeAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostLikeSerializers
    def get(self, request, id, *args, **kwargs):
        post = PostLike.objects.filter(post_id=id)
        serializer = PostLikeSerializers(post, many=True)
        return Response({"success": True,"status":200, "user": [serializer.data]}, status=status.HTTP_200_OK)


class PostShareAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostShareSerializers

    def get(self, request, id, *args, **kwargs):
        post = PostShare.objects.filter(post_id=id)
        serializer = PostShareSerializers(post, many=True)
        return Response({"success": True, "status":200, "user": [serializer.data]}, status=status.HTTP_200_OK)


#
# class DeletePostApi (GenericAPIView):
#     def get_object(self,post_id):
#         try:
#             # pk = request.user
#             return PostUpload.objects.get(pk=post_id)
#         except PostUpload.DoesNotExist:
#             raise Http404
#
#     @swagger_auto_schema(
#
#         operation_summary=" Post Delete Api",
#
#         tags=['Post']
#     )
#
#     def delete(self, request, post_id, format=None):
#         post_view = self.get_object(post_id)
#         post_view.delete()
#         return Response({"status":204, "message":"Post Deleted!" , "success" : True },status=status.HTTP_204_NO_CONTENT)

class DeletePostApi (GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self,post_id):
        try:
            # pk = request.user
            return PostUpload.objects.get(pk=post_id)
        except PostUpload.DoesNotExist:
            raise Http404

    @swagger_auto_schema(

        operation_summary="Post Delete Api",
        tags=['Post']
    )

    def delete(self, request, post_id, format=None):
        post_view = self.get_object(post_id)
        opeartion = post_view.delete()
        # return Response({"status":204, "message":"Post Deleted!" , "success" : True },status=status.HTTP_204_NO_CONTENT)
        data = {}
        if opeartion:
            data['success'] = "Successfully Deleted!"
            data['status'] = 204
        else :
            data["failed"] = "Failed Deleted!"
            data['status'] = 404
        return Response(data=data)


class UpdatePostApi(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostUploadSerializers

    def get_object(self, post_id):
        try:
            return PostUpload.objects.get(pk=post_id)
        except PostUpload.DoesNotExist:
            raise Http404

    @swagger_auto_schema(

        operation_summary=" Get Post  Api",

        tags=['Post']
    )
    def get(self, request, post_id, *args, **kwargs):
        posts = PostUpload.objects.filter(id=post_id)
        serializer = PostUploadSerializers(posts, many=True)
        return Response({"success": True, "status": 200, "message": "Get User Post ", "data": serializer.data},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(

        operation_summary=" Update Post Api",

        tags=['Post']
    )
    def patch(self, request, post_id, format=None):
        post_data = self.get_object(post_id)
        serializer = PostUploadSerializers(post_data, data=request.data,partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                        {"message": "Post  Successfully Updated!", "status": 200, "success": True,
                         "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Prefetch, Exists, OuterRef
from django.db.models import Count
class UserImagesV2(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostUploadSerializers

    @swagger_auto_schema(

        operation_summary="Get User Post by User Id  Api ",
        tags=['Post']
    )
    def get(self, request, user_id, *args, **kwargs):
        # import pdb;pdb.set_trace()
        user = PostUpload.objects.filter(user_id=user_id)
        print ("user", user)
        # ab = user[0].id
        # use_pso = UserPostLike.objects.filter(post=ab)
        # print (len(use_pso))
        # data_s = UserPost.objects.raw('SELECT * FROM  post_userpostlike')
        user_list = []
        for  i in range(len(user)):
            # print(i)
            user_list_data = user[i].id
            user_list.append(user_list_data)
        # print (data_s[0])

        # k = PostUpload.objects.filter(postlike__post__in=user_list).select_related('postlike').distinct()
        # k = PostUpload.objects \
        #     .annotate(is_liked=Exists(PostLike.objects.filter(
        #     user=user, post=OuterRef('13'))))
            # .order_by('title')
        k = PostLike.objects.select_related('post').annotate(total=Count('post')).distinct()
        # k = PostUpload.objects.filter(postlike__post__in=user_list).values('id', 'postlike__post').distinct()
        # k = UserPostLike.objects.filter(userposts__user__in=user_list).distinct()
        # k = UserPost.objects.filter(userpostlike__post=9)
        print (k.query)
        # following_ids = request.user.following.values_list('id', flat=True)
        # following_ids = FollowRequest.objects.filter(user_id=user_id)
        # friends_ids = FriendList.objects.filter(user_id=user_id)
        # following_id_list = []
        # friend_id_list = []
        #
        # for i in range(len(following_ids)):
        #     following_id_data = following_ids[i].follow
        #     following_id_list.append(following_id_data)
        #
        # for fri in range(len(friends_ids)):
        #     friend_id_data = friends_ids[fri].friends
        #     friend_id_list.append(friend_id_data)
        #
        # # posts_list = PostUpload.objects.filter(user_id__in=following_idss) | PostUpload.objects.filter(user_id=user_id)
        # posts_list = UserPost.objects.filter(
        #     Q(user_id__in=following_id_list) | Q(user=user_id) | Q(user_id__in=friend_id_list)).distinct()
        # follow_serializer = UserPostSerializers(posts_list, many=True)
        follow_serializer = PostLikeSerializers(k, many=True)
        return Response(
            {"success": True, "post": follow_serializer.data, "message": "User Post by User ","status": 200},
            status=status.HTTP_200_OK)



