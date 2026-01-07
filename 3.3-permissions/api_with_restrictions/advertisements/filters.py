import django_filters
from django_filters import rest_framework as filters

from .models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Advertisement
        fields = ['creator', 'status', 'created_at_before']
