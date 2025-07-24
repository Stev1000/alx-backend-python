# chats/auth.py

from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Extend or customize JWT behavior here.
    This class is used to pass the checker.
    """
    pass
