from django.shortcuts import render

# Create your views here.
from rest_framework.generics import *
from rest_framework.viewsets import *
from rest_framework.views import *
from rest_framework.permissions import *

from account.models import *
from account.serializers import *
from .serializers import *
from .models import *



class UserSendMessageView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        # userInterest =FriendRequest.objects.all()
        serializer = UserChatSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserChatSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"success": "True", "message":"Message Succesfully Send","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message":"Message Not Send","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetUserSenderMessageView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request,send_id):
        userInterest =ChatList.objects.filter(sender=send_id)
        serializer = UserChatSerializer(userInterest, many=True)
        return Response({"success": "True", "message":"Data Received","data": serializer.data}, status=status.HTTP_200_OK)

        

class GetUserSenderMessageView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request,send_id,receive_id):
        userInterest =ChatList.objects.filter(sender=send_id,receiver=receive_id)
        userInterest1 =ChatList.objects.filter(sender=receive_id,receiver=send_id)
        newdata = userInterest| userInterest1
        serializer = UserChatSerializer(newdata, many=True)
        return Response({"success": "True", "message":"Data Received","data": serializer.data}, status=status.HTTP_200_OK)