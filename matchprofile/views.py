from django.shortcuts import render, get_object_or_404
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import *
import random
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from .filters import *

class AddPostUserUpdateView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =PostUserUpdate.objects.all()
        serializer = PostUserUpdateSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = PostUserUpdateSerializer(data=request.data)
        
        if serializer.is_valid():   
                
            serializer.save()
            
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PostUserReactSerializerView(APIView):
    # permission_classes = (AllowAny,)

    def get(self, request):
        userInterest =PostUserReact.objects.all()
        serializer = PostUserReactSerializer(userInterest, many=True)
        return Response({"success": "True", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        
        serializer = PostUserReactSerializer(data=request.data)
        
        if serializer.is_valid():   
            obj = PostUserUpdate.objects.filter(id=1)
            obj = obj[0]
            obj.is_view = obj.is_view + 1
            obj.save(update_fields=("is_view", ))
            serializer.save()
            
            return Response({"success": "True", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


from django.db.models import Q

class MatchProfileUserViewSet(viewsets.ModelViewSet):
    queryset = UserPassion.objects.order_by("-passion")
    serializer_class = UserPassionMatchSerializer
    filterset_class = UserPassionMatchFilter
   
    def get_queryset(self):
        # import pdb;pdb.set_trace()
        queryset = self.queryset

        q_name = Q()
        rel_name = self.request.query_params.get("Art", None)
        if rel_name:
            q_name = Q(users__name=rel_name)

        q_groups = Q()
        rel_groups = self.request.query_params.get("Techlogy", "").split(",")
        if any(rel_groups):
            q_groups = Q(groups__name__in=rel_groups)

        qs = queryset.filter(q_name | q_groups).distinct()
        return qs