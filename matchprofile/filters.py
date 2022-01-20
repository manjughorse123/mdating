from django_filters import rest_framework as rest_framework_filters
from account.models import *

class UserPassionMatchFilter(rest_framework_filters.FilterSet):
    passsion = rest_framework_filters.CharFilter(field_name="passion", lookup_expr="icontains")

    class Meta:
        model = UserPassion
        fields = ("passion", )

