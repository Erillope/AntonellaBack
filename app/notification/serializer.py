from rest_framework import serializers

class AddNotificationTokenSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    token = serializers.CharField()


class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField()
    to = serializers.CharField(max_length=255)