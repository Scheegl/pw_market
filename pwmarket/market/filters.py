from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter
from .models import Lots


class LotsFilter(FilterSet):
    class Meta:
        model = Lots
        fields = {
            'category_choice' : ['icontains'],
        }