from rest_framework import serializers
from .models import User, Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['sender', 'sent_at']  # Sender set in perform_create


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SlugRelatedField(
    many=True,
    slug_field='username',  # 👈 Accept username instead of UUID
    queryset=User.objects.all()
)
    #messages = MessageSerializer(many=True, read_only=True, source='messages')
    messages = MessageSerializer(many=True, read_only=True)


    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'first_name', 'last_name',
            'email', 'password', 'phone_number', 'role', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number'),
            role=validated_data.get('role')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_role(self, value):
        valid_roles = ['guest', 'host', 'admin']
        if value not in valid_roles:
            raise serializers.ValidationError(f"Role must be one of {valid_roles}")
        return value
