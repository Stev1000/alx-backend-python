from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        # For Message object, check via obj.conversation
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()
        # For Conversation object
        return user in obj.participants.all()
