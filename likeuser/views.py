from rest_framework.generics import *

from rest_framework.views import *
from account.models import *
from rest_framework.viewsets import *
from account.serializers import *
from likeuser.serilaizers import *
from matchprofile.models import UserMatchProfile
from .models import *


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
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest = UserLike.objects.all()
        serializer = UserLikeSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        # import pdb;pdb.set_trace()
        serializer = UserLikeSerializer(data=request.data)

        if serializer.is_valid():

            # to_user= serializer.validated_data['to_user']
            # flag= serializer.validated_data['flg']
            # send_requst = UserLike.objects.filter(to_user =to_user )
            # send_requst.update(flg = True)

            serializer.save()

            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLikeNewView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        user = request.data.get('user')
        userInterest = UserLike.objects.filter(user)
        serializer = UserLikeNewSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)


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

        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        friend_req_list = self.get_object(pk)
        friend_req_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.db.models import Q


class MatchUserProfileView(APIView):

    # def get(self, request):

    # def get_object(self, pk):
    #     try:
    #         return UserPassion.objects.filter(user_id=pk)
    #     except UserPassion.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     # import pdb;pdb.set_trace()

    #     follower_info = self.get_object(pk)
    #     userPassion = UserPassion.objects.filter(Q(passion=1) |
    #                                              Q(passion=2) |
    #                                              Q(passion=3) |
    #                                              Q(passion=4) |
    #                                              Q(passion=5) |
    #                                              Q(passion=6) |
    #                                              Q(passion=7) |
    #                                              Q(passion=8) |
    #                                              Q(passion=9) |
    #                                              Q(passion=10) |
    #                                              Q(passion=11))

    #     for i in range(len(follower_info)):
    #         for j in range(len(userPassion)):
    #             ab = follower_info[i].passion
    #             abs = follower_info[i].user
    #             # print ("ab = ",ab,abs)
    #             abb = userPassion[j].passion
    #             abbs = userPassion[j].user
    #             # print ("abb = ",abb,abbs)

    #             if ab == abb:
    #                 if abs != abbs:
    #                     # print (abbs)
    # ad = UserPassion.objects.filter(user=abbs)
    #                     # print (ab)
    #                     # obj =  UserMatchProfile()
    #                     # obj.save()
    #                     # serializer = UserPassionSerializer(ad, many=True)   

    #     return Response({"success": "True", "data": "serializer.data"}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # import pdb;pdb.set_trace()

        follower_info = request.data['user']
        userPassion = UserPassion.objects.filter(Q(passion=1) |
                                                 Q(passion=2) |
                                                 Q(passion=3) |
                                                 Q(passion=4) |
                                                 Q(passion=5) |
                                                 Q(passion=6) |
                                                 Q(passion=7) |
                                                 Q(passion=8) |
                                                 Q(passion=9) |
                                                 Q(passion=10) |
                                                 Q(passion=11))

        follower_info = UserPassion.objects.filter(user=follower_info)
        for i in range(len(follower_info)):
            for j in range(len(userPassion)):
                ab = follower_info[i].passion
                abs = follower_info[i].user
                # print ("ab = ",ab,abs)
                abb = userPassion[j].passion
                abbs = userPassion[j].user
                # print ("abb = ",abb,abbs)

                if ab == abb:
                    # if abs != abbs:
                    # print (abbs)
                    ad = UserPassion.objects.filter(user=abbs)
                    print(ab)
                    obj = UserMatchProfile(user=follower_info, to_user=ad)
                    obj.save()
                    serializer = MatchesprofileSerializer(ad, many=True)

        return Response({"success": "True", "data": "serializer.data"}, status=status.HTTP_200_OK)
