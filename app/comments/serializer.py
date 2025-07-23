from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=500)
    starts = serializers.IntegerField()
    user_id = serializers.UUIDField()
    service_id = serializers.UUIDField()