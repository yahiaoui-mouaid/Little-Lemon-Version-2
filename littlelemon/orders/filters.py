"""
Filtering support for the manager order endpoint.

Requires: pip install django-filter
Add 'django_filters' to INSTALLED_APPS.
"""
import django_filters

from .models import Order


class OrderFilter(django_filters.FilterSet):
    # Category comes from the menu item attached to each order line.
    category = django_filters.CharFilter(
        field_name="items__item__category", lookup_expr="iexact"
    )

    # Price range, based on the order's total_price.
    min_price = django_filters.NumberFilter(field_name="total_price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="total_price", lookup_expr="lte")

    # Time granularity, based on date_ordered.
    year = django_filters.NumberFilter(field_name="date_ordered", lookup_expr="year")
    month = django_filters.NumberFilter(field_name="date_ordered", lookup_expr="month")
    day = django_filters.NumberFilter(field_name="date_ordered", lookup_expr="day")
    hour = django_filters.NumberFilter(field_name="date_ordered", lookup_expr="hour")

    class Meta:
        model = Order
        fields = ["category", "min_price", "max_price", "year", "month", "day", "hour"]


        