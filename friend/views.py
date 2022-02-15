from rest_framework.generics import *
from .serializers import *
from rest_framework.views import *
from .models import *
from rest_framework.viewsets import *



class AddFriendRequestSendView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        # import pdb;pdb.set_trace()
        userInterest =FriendRequest.objects.all()
        serializer = GetFriendRequestSerializer(userInterest, many=True)
        return Response({"success": True, "message" :" User  Send Request Detail" ,"status" :200,"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):

        serializer = FriendRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            sender = serializer.validated_data['sender']
            receiver = serializer.validated_data['receiver']
            obj = FriendRequest.objects.create(receiver=receiver, sender=sender, friendrequestsent=True)
            # serializer.save()

            return Response({"success": True, "message": "Friend Request Sent!","status":201 ,"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": True, "message": "Friend Request  Was Alraedy Sent!","status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddFriendRequestAcceptView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =FriendList.objects.all()
        serializer = FriendListSerializer(userInterest, many=True)
        return Response({"success": True, "message" :" User Accept Request Detail" ,"status": 200,"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FriendListSerializer(data=request.data)
        
        if serializer.is_valid(): 
        
            to_user= serializer.validated_data['user']
            send_requst = FriendRequest.objects.filter(sender =to_user )
            send_requst.update(friendrequestsent = False)
        
            serializer.save()
            
            return Response({"success": True, "message": "Friend Request Accepted!", "status": 201,"data": serializer.data }, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message": "Friend Request was Already Accepted !","status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class GetFriendRequestListView(APIView):
    """
    Retrieve, update or delete a Get Follower instance.
    """

    def get_object(self, pk):
        try:
            return FriendRequest.objects.filter(receiver_id=pk)
        except FriendRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        friend_req_list = self.get_object(pk)
        serializer = FriendRequestListSerializer(friend_req_list, many=True)
        return Response({"success": True, "status": 200 ,"message": "Detail","data": serializer.data, 'data_count' :len(serializer.data)}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        friend_req_list = self.get_object(pk)
        friend_req_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class  AddFollowRequestView(APIView):
    # permission_classes = (AllowAny,)
    def get(self, request):
        userInterest =FollowRequest.objects.all()
        serializer = FollowRequestSerializer(userInterest, many=True)
        return Response({"success": True,"status": 200,"message" :" User follow Request Detail" , "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FollowRequestSerializer(data=request.data)
        
        if serializer.is_valid():   
            serializer.save()
            
            return Response({"success": True, "message": "Follow Request Send","status": 201,"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error",  "message": "Follow Request was Already Send", "status": 400, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FollowRequestAcceptView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        follow_accept =FollowAccept.objects.all()
        serializer = FollowAcceptSerializer(follow_accept, many=True)
        return Response({"success": True,"message" :" User  Accept follow Detail" , "status": 200,"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FollowAcceptSerializer(data=request.data)
        
        if serializer.is_valid(): 
            to_user= serializer.validated_data['follow']
            send_requst = FollowRequest.objects.filter(follow =to_user )
            send_requst.update(is_active = False) 
            serializer.save()
            
            return Response({"success": True, "message": "Follow Request Accept", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message": "Follow Request Already","status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# GetFollowerView
class GetFollowerView(APIView):
    """
    Retrieve, update or delete a Get Follower instance.
    """
    def get_object(self, pk):
        try:
            return FollowRequest.objects.filter(user_id=pk)
        except FollowRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # import pdb;pdb.set_trace()
        follower_info = self.get_object(pk)
        serializer = FollowRequestFollowerSerializer(follower_info, many=True)

        return Response({"success": True, "message" :" User follow Detail" ,"data": serializer.data,"status": 200, 'data_count' :len(serializer.data) }, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        follower_info = self.get_object(pk)
        follower_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Get Following View
class GetFollowingView(APIView):
    """
    Retrieve, update or delete a Get Follower instance.
    """

    def get_object(self, pk):
        try:
            return FollowAccept.objects.filter(user_id=pk)
        except FollowAccept.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):    
        following_list = self.get_object(pk)
        serializer = FollowListFollowingSerializer(following_list, many=True)
        
        return Response({"success": True,"message" :" User Following Detail" , "status": 200,"data": serializer.data ,'data_count' :len(serializer.data) }, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        following_list = self.get_object(pk)
        following_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FAQView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        faq = FAQ.objects.all()
        serializer = FAQSerializer(faq, many=True)
        return Response({"success": True,"message" :" FAQ Data!" , "status": 200 ,"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FAQSerializer(data=request.data)
        
        if serializer.is_valid(): 
            serializer.save()
            
            return Response({"success": True, "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FAQDetailUpdateInfoView(APIView):
    """
    Retrieve, update or delete a Teacher instance.
    """

    def get_object(self, pk):
        try:
            return FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        faq_info = self.get_object(pk)
        serializer = FAQSerializer(faq_info)
        
        return Response({"success": True,"status": 201, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        faq_info = self.get_object(pk)
        serializer = FAQSerializer(faq_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,"status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        faq_info = self.get_object(pk)
        serializer = FAQSerializer(
            faq_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "status": 201,"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        faq_info = self.get_object(pk)
        faq_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        # if serializer.is_valid():
        #     ab = serializer.validated_data['user']
        #     like_profile_user = serializer.validated_data['like_profile_user']
        #     if request.data['flag'] == '1':
        #         if UserMatchProfile.objects.filter(like_profile_user=like_profile_user):
        #             return Response({"success": "error", "status": 400, "message": "User Already like Profile "},
        #                             status=status.HTTP_400_BAD_REQUEST)
        #         else:
        #             obj = UserMatchProfile.objects.create(user = ab,like_profile_user=like_profile_user,is_like = True)
        #
        #     if request.data['flag'] == '2':
        #         if UserMatchProfile.objects.filter(like_profile_user=like_profile_user,is_like =False):
        #
        #             return Response({"success": "error", "status": 400, "message": "User Already Dislike Profile "},
        #                             status=status.HTTP_400_BAD_REQUEST)
        #         else:
        #             obj = UserMatchProfile.objects.filter(user=ab)
        #
        #             obj.is_like = False
        #             # obj.save(update_fields=("is_like",))
        #             obj.update()
        #
        #     if request.data['flag'] == '3':
        #         obj = UserMatchProfile.objects.filter(like_profile_user=like_profile_user)
        #         obj = obj[0].id
        #         objs = UserMatchProfile.objects.filter(id=obj)
        #         objs.delete()
        #         return Response({"success": True,"message": "User Dislike !" ,"status": 200},status=status.HTTP_200_OK)

class AddFriendRequestAcceptDeatilApiView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest = FriendList.objects.all()
        serializer = FriendListSerializer(userInterest, many=True)
        return Response(
            {"success": True, "message": " User Accept Request Detail", "status": 200, "data": serializer.data},
            status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FriendListSerializer(data=request.data)

        if serializer.is_valid():

            ab = serializer.validated_data['user']
            friends = serializer.validated_data['friends']
            if request.data['flag'] == '1':
                # to_user = serializer.validated_data['user']
                # send_requst = FriendRequest.objects.filter(sender=to_user)
                # send_requst.update(friendrequestsent=False)
                if FriendList.objects.filter(friends=friends):
                    return Response({"success": "error", "status": 400, "message": "User Already friend"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    new_friend = FriendList.objects.create(user = ab,friends=friends,is_accepted= True)
                    obj = FriendRequest.objects.filter(sender=friends)
                    obj = obj[0].id
                    objs = FriendRequest.objects.filter(id=obj)
                    objs.delete()

            if request.data['flag'] == '2':
                obj = FriendRequest.objects.filter(sender=friends)
                obj = obj[0].id
                objs = FriendRequest.objects.filter(id=obj)
                objs.delete()
                return Response({"success": True,"message": "Friend Request Deleted !" ,"status": 200},status=status.HTTP_200_OK)

            # serializer.save()

            return Response(
                {"success": True, "message": "Friend Request Accepted!", "status": 201, "data": serializer.data},
                status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message": "Friend Request was Already Accepted !", "status": 400,
                             "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
