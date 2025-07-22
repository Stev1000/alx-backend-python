from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to users who are participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Check if obj is a Message, access its conversation
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()

        # Check if obj is a Conversation
        return user in obj.participants.all()
