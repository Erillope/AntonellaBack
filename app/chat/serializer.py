from rest_framework import serializers
from core.chat.dto import MessageType

class AddChatMessageSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)
    content = serializers.CharField()
    message_type = serializers.ChoiceField(choices=[mt.value for mt in MessageType])