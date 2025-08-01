from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import render
from .models import Message
from django.db.models import Prefetch

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