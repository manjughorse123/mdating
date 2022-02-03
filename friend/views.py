
from rest_framework.generics import *
from .serializers import *
from rest_framework.views import *
from .models import *
from rest_framework.viewsets import *



class AddFriendRequestSendView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =FriendRequest.objects.all()
        serializer = FriendRequestSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FriendRequestSerializer(data=request.data)
        
        if serializer.is_valid():   
                
            serializer.save()

            return Response({"success": "True", "status":201 ,"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "status": 404,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddFriendRequestAcceptView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =FriendList.objects.all()
        serializer = FriendListSerializer(userInterest, many=True)
        return Response({"success": "True", "status": 200,"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FriendListSerializer(data=request.data)
        
        if serializer.is_valid(): 
        
            to_user= serializer.validated_data['user']
            send_requst = FriendRequest.objects.filter(sender =to_user )
            send_requst.update(is_active = False) 
        
            serializer.save()
            
            return Response({"success": "True", "status": 201,"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
        
        return Response({"success": "True", "status": 200 ,"data": serializer.data, 'data_count' :len(serializer.data)}, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        friend_req_list = self.get_object(pk)
        friend_req_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class  AddFollowRequestView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =FollowRequest.objects.all()
        serializer = FollowRequestSerializer(userInterest, many=True)
        return Response({"success": "True","status": 200, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FollowRequestSerializer(data=request.data)
        
        if serializer.is_valid():   
                
            serializer.save()
            
            return Response({"success": "True", "status": 201,"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FollowRequestAcceptView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        follow_accept =FollowAccept.objects.all()
        serializer = FollowAcceptSerializer(follow_accept, many=True)
        return Response({"success": "True", "status": 200,"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FollowAcceptSerializer(data=request.data)
        
        if serializer.is_valid(): 
            to_user= serializer.validated_data['follow']
            send_requst = FollowRequest.objects.filter(follow =to_user )
            send_requst.update(is_active = False) 
            serializer.save()
            
            return Response({"success": "True", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "status": 400,"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



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

        return Response({"success": "True", "data": serializer.data,"status": 200, 'data_count' :len(serializer.data) }, status=status.HTTP_200_OK)

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
        
        return Response({"success": "True", "status": 200,"data": serializer.data ,'data_count' :len(serializer.data) }, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        following_list = self.get_object(pk)
        following_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class FAQView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        faq = FAQ.objects.all()
        serializer = FAQSerializer(faq, many=True)
        return Response({"success": "True", "status": 200 ,"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FAQSerializer(data=request.data)
        
        if serializer.is_valid(): 
            serializer.save()
            
            return Response({"success": "True", "status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
        
        return Response({"success": "True","status": 201, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        faq_info = self.get_object(pk)
        serializer = FAQSerializer(faq_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True","status": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        faq_info = self.get_object(pk)
        serializer = FAQSerializer(
            faq_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "status": 201,"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        faq_info = self.get_object(pk)
        faq_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)