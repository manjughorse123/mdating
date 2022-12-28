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
from account.utils import *


class UserSendMessageView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # userChat =FriendRequest.objects.all()
        serializer = UserChatSerializer(userChat, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserChatSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data1 = User.objects.get(id = request.data['receiver'])
            vals = ChatList.objects.filter(receiver=data1).last()
            
            val =send_notification(vals.sender,body="{}".format(vals.is_text))
            data2 = User.objects.get(id = vals.sender.id)
            NotificationData.objects.create(notify_user=vals.sender,notification_message="{}".format(vals.is_text),user=data1)
            print(val,vals.sender,data2)
            return Response({"success": "True", "message":"Message Succesfully Send","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "message":"Message Not Send","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetUserSenderMessageView12(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,send_id):
        userChat =ChatList.objects.filter(sender=send_id)
        serializer = UserChatSerializer(userChat, many=True)
        return Response({"success": "True", "message":"Data Received","data": serializer.data,"status":200}, status=status.HTTP_200_OK)

        

class GetUserSenderMessageView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,send_id,receive_id):
        user_id = request.user.id
        print (user_id)
        userFind = User.objects.get(id=user_id)
        userChat =ChatList.objects.filter(sender=send_id,receiver=receive_id).order_by('-id').exclude(is_text=None)

        userChat1 =ChatList.objects.filter(sender=receive_id,receiver=send_id).order_by('-id').exclude(is_text=None)
        userChatReadValue =ChatList.objects.filter(receiver=userFind)
        for i in range(len(userChatReadValue)) :
            userChatReadValue[i].is_text_read = True
            userChatReadValue[i].save()
            pass

        newdata = userChat| userChat1
        serializer = UserChatSerializer(newdata, many=True)
        return Response({"success": True, "message":"Data Received","data": serializer.data,"status":200}, status=status.HTTP_200_OK)

class GetUserChatListView(APIView):
    permission_classes = (IsAuthenticated,)    

    # def get(self, request,user_id):
    #     user_ids = request.user.id
    #     print (user_id)
    #     userFind = User.objects.get(id=user_id)
    #     userChatReadValue =ChatList.objects.filter(receiver=userFind,is_text_read=False)
        
    #     userChat =ChatList.objects.filter(sender=user_id).order_by('receiver','-create_at').distinct('receiver')
    #     print(userChat)
    #     # val = userChat
    #     serializer = UserChatNewSerializer(userChat,context={
    #                                          'request': user_id}, many=True)
    #     return Response({"success": True, "message":"Data Received","data": serializer.data,"status":200}, status=status.HTTP_200_OK)

    def get(self, request,user_id):
        user_ids = request.user.id
        print (user_id)
        userFind = User.objects.get(id=user_id)
        userChatReadValue =ChatList.objects.filter(receiver=userFind,is_text_read=False)
        
        userChat =ChatList.objects.filter(receiver=user_id).distinct('sender').order_by('sender','-create_at')
        print(userChat)
        # val = userChat
        serializer = UserChatNewSerializer(userChat,context={
                                             'request': user_id}, many=True)
        return Response({"success": True, "message":"Data Received","data": serializer.data,"status":200}, status=status.HTTP_200_OK)