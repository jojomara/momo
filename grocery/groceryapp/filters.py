import django_filters # type: ignore
from .models import stockx

class StockxFilter(django_filters.FilterSet):
    class Meta:

        model = stockx
        fields = ['item_name']
