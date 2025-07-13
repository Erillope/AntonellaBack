from rest_framework import serializers

class AddNotificationTokenSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    token = serializers.CharField()