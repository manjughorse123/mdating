from rest_framework.serializers import *
from account.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class UserFilterSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = User
        geo_field = "location"
        fields = ('id', 'gender', 'birth_date', 'location')
