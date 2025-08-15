from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'read']
        #read_only_fields = ['read', 'timestamp']  # ✅ Don't allow users to manually set this
