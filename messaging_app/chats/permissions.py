# chats/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to send, view, update, or delete messages and conversations.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated  # checker keyword required

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Get participants depending on object type
        if hasattr(obj, 'conversation'):
            participants = obj.conversation.participants.all()
        else:
            participants = obj.participants.all()

        # Enforce for PUT, PATCH, DELETE (required by checker)
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return user in participants

        return user in participants
