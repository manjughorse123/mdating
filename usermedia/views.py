from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.permissions import *

from usermedia.models import *
from usermedia.serializers import *
from account.models import User


class UserMediaApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GetMediaPostV2Serializers

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

        operation_summary="User Media By User Id",

        tags=['User Media']
    )
    def get(self, request, user_id, *args, **kwargs):

        user = MediaPost.objects.filter(user_id=user_id).order_by('-create_at')
        serializer = GetMediaPostV2Serializers(
            user, context={'request1': request.user.id,'request': request}, many=True)
        return Response({"media": serializer.data, "status": 200, "success": True}, status=status.HTTP_200_OK)


class UserVideoApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GetUserVideoSerialize

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

        operation_summary="User Video By User Id",

        tags=['User Media']
    )
    def get(self, request, user_id, *args, **kwargs):

        user = MediaVideo.objects.filter(user_id=user_id)
        serializer = GetUserVideoSerialize(
            user, context={'request': request.user.id}, many=True)
        return Response({"media": serializer.data, "status": 200, "success": True}, status=status.HTTP_200_OK)


class UserMediaAPIPost(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
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
        serializer = MediaPostSerializers(
            media, context={'request': request}, many=True)
        return Response({"success": True, "status": 200, "post": serializer.data}, status=status.HTTP_200_OK)


class GetMediaUploadApi(GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = GetMediaPostSerializers

    @swagger_auto_schema(

        operation_summary="Get User Media By Media Id  ",

        tags=['User Media']
    )
    def get(self, request, id, *args, **kwargs):
        posts = MediaPost.objects.filter(id=id)
        serializer = MediaPostSerializers(posts, many=True)
        return Response({"status": 200, "success": True, "post": serializer.data}, status=status.HTTP_200_OK)


class MediaUploadApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
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

        operation_summary="Create User Media Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'media': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Media Image'),
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Id'),
                'caption': openapi.Schema(type=openapi.TYPE_STRING, description='Add Caption'),

            }),

        tags=['User Media']
    )
    def post(self, request, *args, **kwargs):
    
        if "user_media" in request.data:
            media = request.data.get('user_media'),
            print(request.data.get('user_media'))
            if 'caption' in request.data:
                user = request.user.id
                obj = User.objects.filter(id=user)
                obj.update(is_media=True)
                # string = request.data['user_media']
                
                # new_caption = request.data['caption']
                # name = string.split(',')
                
                name = request.FILES.getlist('user_media')
                for i in range(len(name)):

                    media_data = MediaPost.objects.create(
                        user=request.user, user_media=name[i], caption=new_caption)

                return Response({"success": True, "message": "User Media Added!", "status": 201, "post": "post"}, status=status.HTTP_201_CREATED)

            else:
                if media is not None:
                    user = request.user.id
                    obj = User.objects.filter(id=user)
                    obj.update(is_media=True)
                    # string = request.data['media']
                    name = request.FILES.getlist('user_media')
                    print(request.data.get('user_media'),request.FILES.getlist('user_media'))
                    for i in range(len(name)):
                        media_data = MediaPost.objects.create(
                            user=request.user, user_media=name[i])

                    return Response({"success": True, "message": "User Media Added!", "status": 201, "post": "post"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": 400, "message": "No Media Found"}, status=status.HTTP_400_BAD_REQUEST)

class MediaUploadV2Api(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
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

        operation_summary="Create User Media Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'media': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Media Data'),

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
            obj = User.objects.filter(id=user)
            obj.update(is_media=True)
            string = request.data['media']
            name = string.split(',')

            for i in range(len(name)):
                media_image = MediaPost.objects.create(
                    user=request.user, media=name[i], caption=caption)
            return Response({"success": True, "message": "User Media Added!", "status": 201, "post": "post"},
                            status=status.HTTP_201_CREATED)
        return Response({"status": 400, "message": "no data found"}, status=status.HTTP_400_BAD_REQUEST)


class MediaReactionApiView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = MediaPostSerializers

    # def get(self, request):
    #     userView = MediaView.objects.all()
    #     userLike = MediaLike.objects.all()
    #     userShare = MediaShare.objects.all()
    #     serializerView = MediaViewSerializers(userView, many=True)
    #     serializerLike = MediaLikeSerializers(userLike, many=True)
    #     serializerShare = MediaShareSerializers(userShare, many=True)
    #     return Response({"success": True, "status":200 ,"data View": serializerView.data, "data Like": serializerLike.data,
    #                      "data share": serializerShare.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(

        operation_summary="Create User Media  Add Reaction Api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'media': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Media Image'),

                'user': openapi.Schema(type=openapi.TYPE_STRING, description='Add User Id '),
                'flag': openapi.Schema(type=openapi.TYPE_STRING, description='Add flag 1 for view Media,2 for like Media'),

            }),

        tags=['User Media']
    )
    def post(self, request, format='json'):
        try:
            user = request.data['user']
            media = request.data['media']
            is_like = request.data['is_like']
            postdata = int(media)
            flag = request.data['flag']
            flagdata = int(flag)
            obj = MediaPost.objects.filter(id=postdata)
            serializerView = MediaViewSerializers(data=request.data)
            serializerLike = MediaLikeSerializers(data=request.data)

            if serializerView.is_valid():
                if flagdata == 1:
                    if MediaView.objects.filter(user=user, media=postdata).exists():
                        return Response(
                            {"message": "User Already Post Viewed",
                                "success": "False", "data": serializerView.data},
                            status=status.HTTP_201_CREATED)

                    else:
                        obj = obj[0]
                        obj.view_count = obj.view_count + 1
                        obj.save(update_fields=("view_count",))
                        serializerView.save()

                        return Response(

                            {"message": "User Post View Successfully", "status": 200,
                                "success": "True", "data": serializerView.data},
                            status=status.HTTP_201_CREATED)
            if serializerLike.is_valid():

                if flagdata == 2:
                    if is_like == True:
                        if MediaLike.objects.filter(user=user, media=postdata).exists():
                            return Response(
                                {"message": "User Already Post Liked",
                                    "success": "False", "data": serializerLike.data},
                                status=status.HTTP_201_CREATED)
                        else:
                            obj = obj[0]
                            obj.like_count = obj.like_count + 1
                            obj.save(update_fields=("like_count",))
                            media_data = MediaLike.objects.create(
                                user_id=user, media_id=postdata, is_like=is_like)
                            # serializerLike.save()

                            return Response(
                                {"message": "User Post Like Successfully",
                                    "success": "True", "data": serializerLike.data},
                                status=status.HTTP_201_CREATED)
                    else:
                        obj = obj[0]
                        obj.like_count = obj.like_count - 1
                        obj.save(update_fields=("like_count",))
                        obs = MediaLike.objects.filter(
                            user_id=user, media_id=postdata)
                        obs = obs[0]
                        obs.delete()
                        return Response(
                            {"message": "User Post disLike Successfully", "status": 200,
                                        "success": True, "user": [serializerLike.data]},
                            status=status.HTTP_200_OK)
            else:
                return Response({"message": "Data Not Valid", "status": 400, "success": "error", "flag": False},
                                status=status.HTTP_400_BAD_REQUEST)
                # return Response({"success": "error", "data": serializerLike.errors}, status=status.HTTP_400_BAD_REQUEST)
                # return Response({"success": "error", "data": serializerShare.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "No Data", "status": 400, "success": "error"},
                            status=status.HTTP_400_BAD_REQUEST)


class MediaViewAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MediaPostSerializers

    def get(self, request, id, *args, **kwargs):
        media = MediaView.objects.filter(media_id=id)
        print(media)
        serializer = MediaViewSerializers(media, many=True)
        return Response({"success": True, "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)


class MediaLikeAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MediaPostSerializers

    def get(self, request, id, *args, **kwargs):
        media = MediaLike.objects.filter(media_id=id)
        print(media)
        serializer = MediaLikeSerializers(media, many=True)
        return Response({"success": True, "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)


class MediaShareAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MediaPostSerializers

    def get(self, request, id, *args, **kwargs):
        media = MediaShare.objects.filter(media_id=id)
        print(media)
        serializer = MediaShareSerializers(media, many=True)
        return Response({"success": True, "status": 200, "data": serializer.data}, status=status.HTTP_200_OK)


class UserMediaDeleteApiView (GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, media_id):

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
        else:
            data["failed"] = "Failed Deleted!"
            data['status'] = 404
        return Response(data=data)


class MediaReportsApiView(GenericAPIView):
    serializer_class = MediaPostReportSerialize
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(

        operation_summary="Media Post Reports Api ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'media': openapi.Schema(type=openapi.TYPE_STRING, description='Add post Id'),
                'report_text': openapi.Schema(type=openapi.TYPE_STRING, description='Add Reports Text'),
            }),

        tags=['Post']
    )
    def post(self, request, format='json'):
        serializer = MediaPostReportSerialize(data=request.data)
        if serializer.is_valid():
            # post_report = serializer.validated_data['post']
            post_request = request.data['media_post']
            post_data = MediaPost.objects.get(id=post_request)
            post_data.media_report = True
            post_data.save()
            serializer.save()

            return Response({"success": True, "message": "Post Reports ", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "NO Data!", "status": 200, "data": serializer.errors}, status=status.HTTP_200_OK)



class UserUpdateMediaView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    # queryset = MediaPost.objects.all()
    serializer_class = MediaPostSerializers


    def put(self,request,*args,**kwargs):
        user_id = request.user.id
        media_id=self.kwargs.get('media_id')
        
        # user_id = self.kwargs.get('user_id')
        userMedia = MediaPost.objects.filter(user_id=user_id,id=media_id).first()
        serializer = MediaPostSerializers(userMedia, data=request.data, partial=True)
        print("request.data", request.data)
   
        if serializer.is_valid():
            user_data = serializer.save()
            return Response({"message": "User Media is Successfully Updated!", "status": 200, "success": True,
                             "data": "user_data"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)