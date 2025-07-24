# chats/middleware.py
import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allow access between 18:00 (6 PM) and 21:00 (9 PM)
        if request.path.startswith('/api/conversations/') and not (18 <= current_hour < 21):
            return HttpResponseForbidden("⛔ Access to chats is only allowed between 6 PM and 9 PM.")

        response = self.get_response(request)
        return response