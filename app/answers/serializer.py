from rest_framework import serializers
    
class AnswerInfoSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000, required=False)
    images = serializers.ListField(
        child=serializers.CharField(max_length=1000),
        required=False
    )    
    
class AnswerSerializer(serializers.Serializer):
    client_id = serializers.UUIDField()
    question_id = serializers.UUIDField()
    service_item_id = serializers.UUIDField()
    answer = AnswerInfoSerializer()
    