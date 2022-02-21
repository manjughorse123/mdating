from friend.models import *
from rest_framework import serializers
# from .serializers import *

class FAQSerializer(serializers.ModelSerializer):

        class Meta:
            model  = FAQ
            fields = "__all__"