import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['start_time', 'end_time', 'sender']
