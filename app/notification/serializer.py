from rest_framework import serializers
from core.common.notification import NotificationType

class AddNotificationTokenSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    token = serializers.CharField()


class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField()
    to = serializers.CharField(max_length=255)
    type = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in NotificationType], default=NotificationType.INSTANTANEA.value, required=False)
    publish_date = serializers.DateTimeField(required=False, allow_null=True)