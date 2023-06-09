from django.db.models import Count
from django.db.models import Q
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from account.utils import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.viewsets import *
from rest_framework.parsers import *
from rest_framework.permissions import *
from DatingApp.baseurl import base_url
from post.models import *
from post.serializers import *
from friend.models import *
from masterapp.models import *

class GetPostUploadApi(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostUploadSerializers

    @swagger_auto_schema(

        operation_summary="Get All Post by Post id",
        tags=['Post']
    )
    def get(self, request, post_id, *args, **kwargs):
        posts = PostUpload.objects.filter(id=post_id)
        serializer = PostUploadSerializers(posts, many=True)
        return Response({"success": True, "status": 200, "message": "User Post by Post ID", "data": serializer.data}, status=status.HTTP_200_OK)


class CreatePostApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostUploadCreateSerializers

    @swagger_auto_schema(

        operation_summary="Create Post Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post': openapi.Schema(type=openapi.TYPE_STRING, description='Add Post Data'),
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='User Id'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Add Suitable Title'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Add Message'),
            }),

        tags=['Post']
    )
    def post(self, request, *args, **kwargs):
        # title = request.data.get('title'),
        # message = request.data.get('message'),
        # post = request.data.get('post'),
        # # 'user': request.data.get('user')
        # user = request.user.id

        # if post is not None:
        #     user = request.user.id
        #     string = request.data['post']
        #     name = string.split(',')

        #     post_uploads = PostUpload.objects.create(
        #         user=request.user, post=string, message=message, title=title)
        #     return Response({"success": True, "message": "User Post Added!", "status": 201, "post": "post"}, status=status.HTTP_201_CREATED)

        #     # for i in range(len(name)):
        #     #     post_uploads = PostUpload.objects.create(user=request.user,post=name[i],message=message, title=title)
        #     # return Response({"success": True, "message": "User Post Added!","status": 201,"post": "post"}, status=status.HTTP_201_CREATED)
        # return Response({"status": 400, "message": False}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PostUploadSerializers(
            data=request.data)
        # print("request.data----------------->",request.data)
        if serializer.is_valid():
            serializer.save()
            val = PostUpload.objects.filter(title=request.data['title']).last()
            name = request.FILES.getlist('post_image')
            
            for i in range(len(name)):
                
                if 'image/png' in  name[i].content_type:
                    PostImageUpload.objects.create(user_post_image=name[i],post_image=val,user_post_type=name[i].content_type)
                else : 

                    PostImageUpload.objects.create(user_post_image=name[i],post_image=val,user_post_type=name[i].content_type)
                
            # PostImageUpload.objects.create(user_post_image=request.data['post_image'],post_image=val)

            return Response({"message":"User Post by User","success":True, "status": 201, "post": [serializer.data]}, status=status.HTTP_201_CREATED)
        return Response({"message": False, "status": 400, "post": [serializer.errors]}, status=status.HTTP_400_BAD_REQUEST)


class NewPostUploadApi(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = NewPostUploadSerializers

    @swagger_auto_schema(

        operation_summary="Create Post Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post': openapi.Schema(type=openapi.TYPE_STRING, description='Add Post Data'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Add Title'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Add Message'),
            }),

        tags=['Post']
    )
    def post(self, request, *args, **kwargs):

        # 'user': request.data.get('user')
        user = request.user.id
        serializer = NewPostUploadSerializers(data=request.data)
        if serializer.is_valid():

            post_upload = PostUpload.objects.create(
                user=request.user, post=request.data['post'], message=request.data['message'], title=request.data['title'])

            return Response({"message": True, "status": 201, "post": [serializer.data]}, status=status.HTTP_201_CREATED)
        return Response({"message": False, "status": 400, "post": [serializer.errors]}, status=status.HTTP_400_BAD_REQUEST)


class UserImagesApiViewV2(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
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

        operation_summary="User Post by User, User Friends and following by user",
        tags=['Post']
    )
    def get(self, request, user_id, *args, **kwargs):
        # user_id = request.user.id
        user = PostUpload.objects.filter(user_id=user_id)
        # following_ids = request.user.following.values_list('id', flat=True)
        following_ids = FollowRequest.objects.filter(user_id=user_id)
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

        follow_serializer = PostUploadSerializers(
            posts_list, context={'request': request}, many=True)

        return Response({"success": True, 'post': follow_serializer.data, "message": "User Post by User ", "status": 200}, status=status.HTTP_200_OK)


class PostReactionApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostViewSerializers

    @swagger_auto_schema(

        operation_summary="Create Post Reaction Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post': openapi.Schema(type=openapi.TYPE_STRING, description='Add Post Data'),
                'flag': openapi.Schema(type=openapi.TYPE_STRING, description='Add flag  1 for view, flag 2 for like if is_like True and flag 2 for Unlike if is_like False'),

            }),

        tags=['Post']
    )
    def post(self, request, format='json'):

        users = request.user.id
        user = User.objects.get(id=str(users))

        if 'post' in request.data:
          
            postdata = int(request.data.get('post'))
            post = PostUpload.objects.get(id=postdata)
            flag = request.data.get('flag')
            flagdata = int(flag)
            obj = PostUpload.objects.filter(id=postdata)
            serializerView = PostViewSerializers(data=request.data)
            serializerLike = PostLikeSerializers(data=request.data)
            # serializerShare = PostShareSerializers(data=request.data)
            if serializerView.is_valid():
                # import pdb;pdb.set_trace()
                if flagdata == 1:
                    if PostView.objects.filter(user=user, post=post).exists():
                        return Response(
                            {"message": "User Already Post Viewed", "status": 200,
                                "success": False, "user": [serializerView.data]},
                            status=status.HTTP_200_OK)

                    else:
                        obj = obj[0]
                        obj.is_view_count = obj.is_view_count + 1
                        obj.save(update_fields=("is_view_count",))
                        PostView.objects.create(user=user, post=post)
                        user_datas = post.user
                        if user != user_datas:
                            val =send_notification2(obj.user,body="{} Viewed Your Post".format(user.name),vals=user,data="SingleUserPost",post=post.id)
                            NotificationData.objects.create(user = obj.user,notification_message="{} Viewed Your Post".format(user.name),notify_user=user,post=post)
                        # serializerView.save()

                        return Response(
                            {"message": "User Post View Successfully", "status": 201,
                                "success": True, "user": [serializerView.data]},
                            status=status.HTTP_201_CREATED)
            if serializerLike.is_valid():
                if flagdata == 2:
                    if request.data.get('is_like') == True:
                        if PostLike.objects.filter(user=user, post=post).exists():

                            return Response(
                                {"message": "User Already Post Liked", "status": 200,
                                    "success": False, "user": [serializerLike.data]},
                                status=status.HTTP_200_OK)

                        else:

                            obj = obj[0]
                            obj.is_like_count = obj.is_like_count + 1
                            obj.save(update_fields=("is_like_count",))
                            
                            user_datas = post.user
                            if user != user_datas:
                                # return True
                                val =send_notification2(obj.user,body="{} Liked Your Post".format(user.name),vals=user,data="SingleUserPost",post=post.id)
                                NotificationData.objects.create(user = obj.user,notification_message="{} Liked Your Post".format(user.name),notify_user=user,post=post)
                                print(val,user)
                            PostLike.objects.create(
                                user=user, post=post, is_like=True)
                        # serializerLike.save()

                            return Response(
                                {"message": "User Post Like Successfully", "status": 201,
                                 "success": True, "user": [serializerLike.data]},
                                status=status.HTTP_201_CREATED)
                    else:
                        if PostLike.objects.filter(user=user, post=post).exists():
                            obj = obj[0]
                            obj.is_like_count = obj.is_like_count - 1
                            obj.save(update_fields=("is_like_count",))
                            obj_like = PostLike.objects.filter(
                                user=user, post=post)
                            obj_like = obj_like[0]
                            obj_like.is_like = False
                            obj_like.save(update_fields=("is_like",))
                            obj_like.delete()
                            return Response(
                                {"message": "User Post disLike Successfully", "status": 200,
                                    "success": True, "user": [serializerLike.data]},
                                status=status.HTTP_200_OK)
                        else:
                            return Response(
                                {"message": "no data found!", "status": 200,
                                    "success": False, "user": [serializerLike.data]},
                                status=status.HTTP_200_OK)

            if serializerShare.is_valid():
                if flagdata == 3:
                    obj = obj[0]
                    obj.is_share_count = obj.is_share_count + 1
                    obj.save(update_fields=("is_share_count",))
                    serializerShare.save()

                    return Response(
                        {"message": "User Post Shared Successfully", "status": 201,
                            "success": True, "user": [serializerLike.data]},
                        status=status.HTTP_201_CREATED)

            else:
                return Response({"success": False, "message": " Not Valid Input !!", "user": [serializerLike.data]}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": " Not Valid Input !!", "success": False, "status": 200},
                        status=status.HTTP_200_OK)

# class AllPostAPI(ListAPIView):
#     queryset = PostUpload.objects.all()
#     serializer_class = PostUploadSerializers


class GetPostViewdetailView(GenericAPIView):
    permission_classes = [AllowAny, ]
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

        operation_summary="Get Post  View Detail Api",

        tags=['Post']
    )
    def get(self, request, pk, format=None):

        post_view = self.get_object(pk)
        serializer = PostViewSerializers(post_view)
        return Response({"success": True, "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)

    # def delete(self, request, pk, format=None):
    #     post_view = self.get_object(pk)
    #     post_view.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)







class UserPostVideoApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostImageUploadVedioSerilaizer
    """
    Retrieve, update or delete  a media instance.
    """

    
    def get(self, request, user_id, format=None):
        

        # user = PostUpload.objects.filter(user_id=user_id)
        ad  = PostUpload.objects.filter(user_id=user_id)
        list1 = []
        for i in range(len(ad)):
            # user = User.objects.filter(id= ad[i].user.id)
            setData = PostImageUpload.objects.filter(post_image=ad[i],user_post_type='video/mp4')

            datas = PostImageUploadVedioSerilaizer(setData,context={'request1': request.user.id},many= True)
            if len(datas.data) > 0 :

                list1.append(datas.data[0])
        # print(list1)   
        # print(request.user.id)
        # serializer = PostUploadVideoSerializers(
        #     user, context={'request': request.user.id}, many=True)
        return Response({"success": True, "status": 200, "data": list1 ,"message" : "User Video Post "}, status=status.HTTP_200_OK)



class AllPostAPI(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    serializer_class = PostUploadSerializers

    @swagger_auto_schema(

        operation_summary="Get All User Post",

        tags=['Post']
    )
    def get(self, request, *args, **kwargs):
        post = PostUpload.objects.all()
        serializer = PostUploadSerializers(post, many=True)
        return Response({"success": True, "status": 200, "message": "All Users Post!", "post": serializer.data}, status=status.HTTP_200_OK)


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

class DeletePostApiView (GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, post_id):
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
        else:
            data["failed"] = "Failed Deleted!"
            data['status'] = 404
        return Response(data=data)


class UpdatePostApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostUploadUpdateSerializers

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
        serializer = PostUploadUpdateSerializers(
            posts, context={'request': request}, many=True)
        return Response({"success": True, "status": 200, "message": "Get User Post ", "data": serializer.data},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(

        operation_summary=" Update Post Api",

        tags=['Post']
    )
    # def patch(self, request, post_id, format=None):
    #     post_data = self.get_object(post_id)
    #     serializer = PostUploadUpdateSerializers(
    #         post_data, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             {"message": "Post  Successfully Updated!", "status": 200, "success": True,
    #              "data": serializer.data})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, post_id, format=None):
       
        post_data = self.get_object(post_id)
        serializer = PostUploadUpdateSerializers(
            post_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            val = PostUpload.objects.filter(id=post_id)
            name = request.FILES.getlist('user_post_image')
            if 'image_ids' in request.data:
                if request.data['image_ids']:
                    abc=     request.data['image_ids']
                    ass = abc.replace("," , " ")
                    ab1 = list(ass.split(" "))
                    val1 = PostImageUpload.objects.filter(id__in=ab1)
                    
                    for i in range(len(name)):
                        val12 = val1
                        # media_data = MediaPost.objects.create(
                        #     user=request.user, user_media=name[i], caption=new_caption)
                        # valse = PostImageUpload.objects.get(id=val12[i].id)
                        if len(ab1)-1 >= i  :
                            valse = PostImageUpload.objects.get(id=int(ab1[i]))
                            valse.user_post_image=name[i]
                            valse.save()
                        else :
                            # val122 = PostUpload.objects.filter(id=val[0].id)
                            PostImageUpload.objects.create(user_post_image=name[i],post_image=val[0])

                else :
                                # val122 = PostUpload.objects.filter(id=val[0].id)
                    for i in range(len(name)):
                        PostImageUpload.objects.create(user_post_image=name[i],post_image=val[0])
            else :
                                # val122 = PostUpload.objects.filter(id=val[0].id)
                    for i in range(len(name)):
                        PostImageUpload.objects.create(user_post_image=name[i],post_image=val[0])
            return Response(
                {"message": "Post  Successfully Updated!", "status": 200, "success": True,
                 "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserImagesV2(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostUploadSerializers

    @swagger_auto_schema(

        operation_summary="User Post by User, User Friends and following by user",
        tags=['Post']
    )
    def get(self, request, user_id, *args, **kwargs):

        user = PostUpload.objects.filter(user_id=user_id)

        # ab = user[0].id
        # use_pso = UserPostLike.objects.filter(post=ab)
        # print (len(use_pso))
        # data_s = UserPost.objects.raw('SELECT * FROM  post_userpostlike')
        user_list = []
        for i in range(len(user)):
            # print(i)
            user_list_data = user[i].id
            user_list.append(user_list_data)
        # print (data_s[0])

        # k = PostUpload.objects.filter(postlike__post__in=user_list).select_related('postlike').distinct()
        # k = PostUpload.objects \
        #     .annotate(is_liked=Exists(PostLike.objects.filter(
        #     user=user, post=OuterRef('13'))))
            # .order_by('title')
        k = PostLike.objects.select_related(
            'post').annotate(total=Count('post')).distinct()
        # k = PostUpload.objects.filter(postlike__post__in=user_list).values('id', 'postlike__post').distinct()
        # k = UserPostLike.objects.filter(userposts__user__in=user_list).distinct()
        # k = UserPost.objects.filter(userpostlike__post=9)
        # print(k.query)
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
            {"success": True, "post": follow_serializer.data,
                "message": "User Post by User ", "status": 200},
            status=status.HTTP_200_OK)
from rest_framework import pagination
class CustomPagination(pagination.PageNumberPagination):
    
    page_query_param = "offset"   # this is the "page"
    page_size_query_param="limit" # this is the "page_size"
    page_size = 10
    max_page_size = 100
    # default_limit = 2
    # limit_query_param = 'limit'
    # offset_query_param = 'offset'
    # max_limit = 50
    
    def get_paginated_response(self, data1):
        return Response({
           
            'post': data1,"success": True,
            
             "message": "User Post by User ", "status": 200,'base_url':base_url},
        status=status.HTTP_200_OK)


# Version 2 API
class UserImagesApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination
    serializer_class = PostUploadV2Serializers

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

        operation_summary="Get User Post by User Id  Api ",
        tags=['Post']
    )
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user_data = User.objects.filter(id=user_id)
        # user = PostUpload.objects.filter(user_id=user_id)
        # following_ids = request.user.following.values_list('id', flat=True)
        # following_ids = FollowRequest.objects.filter(user_id=user_id)
        # friends_ids = FriendList.objects.filter(user_id=user_id)
        # # following_id_list = []
        # # # friend_id_list = []
        # # for i in range(len(following_ids)):
        # #     following_id_data = following_ids[i].follow
        # #     following_id_list.append(following_id_data)

        # # for fri in range(len(friends_ids)):
        # #     friend_id_data = friends_ids[fri].friends
        # #     friend_id_list.append(friend_id_data)

    
        # following_id_list = [following_ids[i].follow for i in range(len(following_ids))]
        # friend_id_list = [friends_ids[fri].friends for fri in range(len(friends_ids)) ]

        user_post_lists = User.objects.filter(Q(gender=user_data[0].gender) |
                                                  Q(passion__in=user_data[0].passion.all(
                                                  ))
                                                  & Q(is_complete_profile=True)
                                                  ).exclude(id=request.user.id).distinct()

        # user_id_list = []
        # for i in range(len(user_post_lists)):
        #     user_posts_lists = user_post_lists[i].id
        #     user_id_list.append(user_posts_lists)

        user_id_list = [user_post_lists[i].id for i in range(len(user_post_lists))]

        # posts_list = PostUpload.objects.filter(
        #     Q(user_id__in=following_id_list)
        #     | Q(user=user_id)
        #     | Q(user_id__in=friend_id_list)| Q(user_id__in=user_id_list),is_soft_delete=False).order_by(
        #     '-create_at').distinct()
        posts_list = PostUpload.objects.filter(
            
             Q(user=user_id)
           | Q(user_id__in=user_id_list),is_soft_delete=False).order_by(
            '-create_at').distinct()

        if len(posts_list) > 0:
            
            user_posts = PostUploadV2Serializers(
                posts_list, context={'request': request}, many=True)
            newsDeta = self.paginate_queryset(user_posts.data)
            newsDeta = self.get_paginated_response(newsDeta)
            
            return newsDeta
        # user_posts = ass
        else:
            # pass
            user_post_lists = User.objects.filter(Q(gender=user_data[0].gender) |
                                                  Q(passion__in=user_data[0].passion.all(
                                                  ))
                                                  & Q(is_complete_profile=True)
                                                  ).exclude(id=request.user.id).distinct()

            user_id_list = [user_post_lists[i].id for i in range(len(user_post_lists))]
            # print("user_post_lists", user_post_lists)

            posts_lists = PostUpload.objects.filter(Q(user_id__in=user_id_list, is_private=0)).order_by(
                '-create_at').exclude(id=request.user.id).distinct()
        
            user_posts = PostUploadV2Serializers(
                posts_lists, context={'request': request}, many=True)
            newsDeta = self.paginate_queryset(user_posts.data)
            newsDeta = self.get_paginated_response(newsDeta)
            
        return newsDeta
        # return Response(
        #     {"success": True, 'post': user_posts.data,
        #         "message": "User Post by User ", "status": 200,'base_url':base_url},
        #     status=status.HTTP_200_OK)


# PostMultipleImageApi
class PostMultipleImageApi(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    # serializer_class = MediaPostSerializers

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

        operation_summary="Create User Media Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'media': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Media Data'),
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='Add user'),
                'caption': openapi.Schema(type=openapi.TYPE_STRING, description='Add Caption'),

            }),

        tags=['User Media']
    )
    def post(self, request, *args, **kwargs):

        # user=request.user.id

        caption = request.data.get('caption'),
        media = request.data.get('media'),
        if media is not None:
            user = request.user.id
            # obj = User.objects.filter(id=user)
            # obj.update(is_media=True)
            string = request.data['media']
            name = string.split(',')

            for i in range(len(name)):
                post_image = PostImage.objects.create(
                    user=request.user, media=name[i], caption=caption)
            return Response({"success": True, "message": "User Media Added!", "status": 201, "post": "post"}, status=status.HTTP_201_CREATED)
        return Response({"status": 400, "message": False}, status=status.HTTP_400_BAD_REQUEST)


class UserAllPostApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostUploadV2Serializers
    pagination_class = CustomPagination

    @swagger_auto_schema(

        operation_summary="Get User Post by User Id  Api ",
        tags=['Post']
    )
    def get(self, request, user_id, *args, **kwargs):
        # user_id = request.user.id
        user = PostUpload.objects.filter(user_id=user_id)
        # following_ids = request.user.following.values_list('id', flat=True)

        posts_list = PostUpload.objects.filter(user=user_id).order_by(
            '-create_at').distinct()

        posts_data = PostUploadV2Serializers(
            posts_list, context={'request': request}, many=True)
        # posts_data = ass

        newsDeta = self.paginate_queryset(posts_data.data)
        newsDeta = self.get_paginated_response(newsDeta)
            
        return newsDeta
        # return Response(
        #     {"success": True, 'post': posts_data.data,
        #         "message": "User Post by User ", "status": 200},
        #     status=status.HTTP_200_OK)


class PostReportsApiView(GenericAPIView):
    serializer_class = NewPostReportSerializers
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(

        operation_summary="Post Reports Api ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post': openapi.Schema(type=openapi.TYPE_STRING, description='Add post Id'),
                'report_text': openapi.Schema(type=openapi.TYPE_STRING, description='Add Report Text'),
            }),

        tags=['Post']
    )
    def post(self, request, format='json'):
        serializer = NewPostReportSerializers(data=request.data)
        if serializer.is_valid():
            post_request = request.data['post']
            post_data = PostUpload.objects.get(id=post_request)
            post_data.post_report = True
            post_data.save()
            serializer.save()

            return Response({"success": True, "message": "Post Reports ", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "NO Data!", "status": 200, "data": serializer.errors}, status=status.HTTP_200_OK)


class UserAllPrivatePostApi(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostUploadV2Serializers

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

        operation_summary="Get User Post by User Id  Api ",
        tags=['Post']
    )
    def get(self, request, user_id, is_private_key, *args, **kwargs):

        is_private_key = str(is_private_key)
        if "1" in is_private_key:

            posts_list = PostUpload.objects.filter(user=user_id, is_private=1).order_by(
                '-create_at').distinct()

            user_posts = PostUploadV2Serializers(
                posts_list, context={'request': request}, many=True)

            return Response(
                {"success": True, 'post': user_posts.data,
                 "message": "User Private Post", "status": 200},
                status=status.HTTP_200_OK)
        else:
            posts_list = PostUpload.objects.filter(user=user_id, is_private=0).order_by(
                '-create_at').distinct()

            user_posts = PostUploadV2Serializers(
                posts_list, context={'request': request}, many=True)

            return Response(
                {"success": True, 'post': user_posts.data,
                 "message": "User Public Post ", "status": 200},
                status=status.HTTP_200_OK)



class UpdatePostImageApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostImageUploadSerilaizer

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

    def get_object(self, post_id):
        try:
            return PostImageUpload.objects.get(pk=post_id)
        except PostImageUpload.DoesNotExist:
            raise Http404

    @swagger_auto_schema(

        operation_summary=" Get Post  Api",

        tags=['Post']
    )
    def get(self, request, post_id, *args, **kwargs):
        posts = PostImageUpload.objects.filter(id=post_id)
        serializer = PostImageUploadSerilaizer(
            posts, context={'request': request}, many=True)
        return Response({"success": True, "status": 200, "message": "Update post image upload", "data": serializer.data},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(

        operation_summary=" Update Post Api",

        tags=['Post']
    )
    def patch(self, request, post_id, format=None):
      
        post_data = self.get_object(post_id)
        posts = PostImageUpload.objects.filter(id=post_id).last()
        postCaption = PostUpload.objects.get(id= posts.post_image.id)
        if 'message' in request.data:
            postCaption.message= request.data['message']
        if 'title' in request.data:
            postCaption.title= request.data['title']
        
        postCaption.save() 
        serializer = PostImageUploadSerilaizer(
            post_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Post  Successfully Updated!", "status": 200, "success": True,
                 "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class DeletePostImageApiView (GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, post_id):
        try:
            # pk = request.user
            return PostImageUpload.objects.get(pk=post_id)
        except PostImageUpload.DoesNotExist:
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
        else:
            data["failed"] = "Failed Deleted!"
            data['status'] = 404
        return Response(data=data)



class GetPostApiView(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = PostUploadUpdateSerializers

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
        serializer = PostUploadUpdateSerializers(
            posts, context={'request': request}, many=True)
        return Response({"success": True, "status": 200, "message": "Get User Post ", "data": serializer.data,"base_url":base_url},
                        status=status.HTTP_200_OK)



class UserReportPostApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostUploadV2Serializers

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

    # def get_object(self:
    #     try:
    #         return NewPostReport.objects.get(pk=post_id)
    #     except NewPostReport.DoesNotExist:
    #         raise Http404

    @swagger_auto_schema(

        operation_summary=" Get Post  Api",

        tags=['Post']
    )
    def get(self, request,  *args, **kwargs):
        posts = PostUpload.objects.filter(user= request.user.id,post_report=True)
        serializer = PostUploadV2Serializers(
            posts, context={'request': request}, many=True)
        return Response({"success": True, "status": 200, "message": "User Reports Post", "data": serializer.data,"base_url":base_url},
                        status=status.HTTP_200_OK)





class UserRepostPostApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = NewPostReportSerializers

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

    # def get_object(self, post_id):
    #     # import pdb;pdb.set_trace()
    #     try:
    #         return NewPostReport.objects.get(pk=post_id)
    #     except NewPostReport.DoesNotExist:
    #         raise Http404

   

    
    def patch(self, request, post_id, format=None):
        
        
        post_data = NewPostReport.objects.filter(post=post_id).first()
        serializer = NewPostReportSerializers(
            post_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User Request for RePost", "status": 200, "success": True,
                 "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



            

class UserReportUndoApiView(GenericAPIView):
    serializer_class = NewPostReportSerializers
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(

        operation_summary="Post Reports Api ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post': openapi.Schema(type=openapi.TYPE_STRING, description='Add post Id'),
                'report_text': openapi.Schema(type=openapi.TYPE_STRING, description='Add Report Text'),
            }),

        tags=['Post']
    )
    def post(self, request, format='json'):
        serializer = NewPostReportSerializers(data=request.data)
        try :
            if serializer.is_valid():
                post_request = request.data['post']
                val = NewPostReport.objects.filter(post=post_request,report_user=request.data['report_user']).last()
                val.delete()
                
                # serializer.save()

                return Response({"success": True, "message": "Post Reports ", "status": 201, "data": {}}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success": False, "message": "NO Data!", "status": 200, "data": serializer.errors}, status=status.HTTP_200_OK)
        except :
            return Response({"success": False, "message": "NO Data!", "status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
