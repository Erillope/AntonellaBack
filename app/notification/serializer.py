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
    redirect_to = serializers.CharField(max_length=255, required=False, allow_blank=True)
    notification_type = serializers.CharField(max_length=50, required=False, allow_blank=True)


class NotificationFilterSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True)
    type = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in NotificationType], required=False, allow_null=True)
    start_date = serializers.DateTimeField(required=False, allow_null=True)
    end_date = serializers.DateTimeField(required=False, allow_null=True)
    limit = serializers.IntegerField(required=False)
    offset = serializers.IntegerField(required=False)
    only_count = serializers.BooleanField(required=False, default=False)