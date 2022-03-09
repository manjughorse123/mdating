from rest_framework.generics import *

from rest_framework.views import *
from account.models import *
from rest_framework.viewsets import *
from account.serializers import *
from likeuser.serilaizers import *
from matchprofile.models import UserMatchProfile
from .models import *
from rest_framework.permissions import  *


# class AddFriendRequestSendView(APIView):
#     # permission_classes = (AllowAny,)

#     def get(self, request):
#         userInterest =FriendRequest.objects.all()
#         serializer = FriendRequestSerializer(userInterest, many=True)
#         return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

#     def post(self, request, format='json'):
#         serializer = FriendRequestSerializer(data=request.data)

#         if serializer.is_valid():

#             serializer.save()

#             return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLikeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        userInterest = UserLike.objects.all()
        serializer = UserLikeSerializer(userInterest, many=True)
        return Response({"success": True, "status": 200,"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        # import pdb;pdb.set_trace()
        serializer = UserLikeSerializer(data=request.data)

        if serializer.is_valid():

            # to_user= serializer.validated_data['to_user']
            # flag= serializer.validated_data['flg']
            # send_requst = UserLike.objects.filter(to_user =to_user )
            # send_requst.update(flg = True)

            serializer.save()

            return Response({"success": True, "status": 201,"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLikeNewView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user = request.data.get('user')
        userInterest = UserLike.objects.filter(user)
        serializer = UserLikeNewSerializer(userInterest, many=True)
        return Response({"success": "True","status": 200, "data": serializer.data}, status=status.HTTP_200_OK)


class GetUserLikeView(APIView):
    """
    Retrieve, update or delete a Get Follower instance.
    """

    def get_object(self, pk):
        try:
            return UserLike.objects.filter(user=pk)
        except UserLike.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        friend_req_list = self.get_object(pk)
        serializer = UserLikeflagSerializer(friend_req_list, many=True)

        return Response({"success": True, "status": 200,"data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        friend_req_list = self.get_object(pk)
        friend_req_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


