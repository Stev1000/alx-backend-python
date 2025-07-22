import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sent_after = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')
    conversation_id = django_filters.NumberFilter(field_name="conversation__id")

    class Meta:
        model = Message
        fields = ['conversation_id', 'sent_after', 'sent_before']
