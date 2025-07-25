# chats/middleware.py

import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
from collections import defaultdict
from threading import Lock

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

        if request.path.startswith('/api/conversations/') and not (0 <= current_hour <= 23):
            return HttpResponseForbidden("Access to chats is only allowed between 6 PM and 9 PM.")

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_per_ip = defaultdict(list)
        self.lock = Lock()
        self.limit = 5  # Max messages per minute
        self.time_window = 60  # 60 seconds

    def __call__(self, request):
        if request.method == 'POST' and '/api/conversations/' in request.path and request.path.endswith('/messages/'): 
            ip_address = self.get_client_ip(request)
            current_time = time.time()

            with self.lock:
                # Remove old timestamps
                self.requests_per_ip[ip_address] = [
                    t for t in self.requests_per_ip[ip_address] if current_time - t < self.time_window
                ]

                if len(self.requests_per_ip[ip_address]) >= self.limit:
                    return JsonResponse(
                        {"error": "Message limit exceeded. Please wait before sending more messages."},
                        status=429
                    )

                self.requests_per_ip[ip_address].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
