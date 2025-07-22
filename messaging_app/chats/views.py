from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant  # custom permission

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]  # Added custom permission
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Only return conversations the authenticated user participates in
        return Conversation.objects.filter(participants__user_id=self.request.user.user_id)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # You may add IsParticipant here if doing object-level checks
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']

    def get_queryset(self):
        # Only return messages in conversations the user is part of
        return Message.objects.filter(conversation__participants__user_id=self.request.user.user_id)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
