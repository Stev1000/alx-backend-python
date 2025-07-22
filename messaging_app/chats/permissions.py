from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Conversation


class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # Case: checking if user is part of the conversation for Message or Conversation object
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False

    def has_permission(self, request, view):
        # Global permission to ensure only authenticated users access the views
        return request.user and request.user.is_authenticated
