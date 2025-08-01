from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse

User = get_user_model()

@require_POST
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('account_deleted')  # You can define a simple success page/view

def account_deleted(request):
    return HttpResponse("Your account and related data have been deleted.")