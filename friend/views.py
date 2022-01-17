
from rest_framework.generics import *
from .serializers import *
from rest_framework.views import *
from .models import *
from rest_framework.viewsets import *



class AddUserInterestView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =FriendList.objects.all()
        serializer = FriendListSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = FriendListSerializer(data=request.data)
        
        if serializer.is_valid():        
            serializer.save()
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
