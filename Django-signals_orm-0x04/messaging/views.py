from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import render
from .models import Message
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

User = get_user_model()

@require_POST
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('account_deleted')  # You can define a simple success page/view

def account_deleted(request):
    return HttpResponse("Your account and related data have been deleted.")

@login_required
def threaded_conversations(request):
    sent_by_user = Message.objects.filter(sender=request.user).select_related('receiver')
    messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
    
    context = {
        'messages': messages
    }
    return render(request, 'messaging/threaded_conversations.html', context)
def get_replies_recursive(message):
    replies_data = []
    for reply in message.replies.all():
        replies_data.append({
            'id': reply.id,
            'sender': reply.sender.username,
            'content': reply.content,
            'timestamp': reply.timestamp,
            'replies': get_replies_recursive(reply)
        })
    return replies_data

class UnreadMessagesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.unread.unread_for_user(self.request.user).only('id', 'sender', 'content', 'timestamp')

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @method_decorator(cache_page(60))  # ✅ Cache this view for 60 seconds
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)