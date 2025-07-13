from django.shortcuts import render
from .models import UserNotificationToken
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .serializer import AddNotificationTokenSerializer

class NotificationTokenView(APIView):
    @validate(AddNotificationTokenSerializer)
    def post(self, request: AddNotificationTokenSerializer) -> Response:
        user_id = request.validated_data['user_id']
        token = request.validated_data['token']
        
        notification_token, created = UserNotificationToken.objects.get_or_create(
            user_id=user_id,
            defaults={'token': token}
        )
        
        if not created:
            notification_token.token = token
            notification_token.save()
        
        return success_response({"user_id": str(notification_token.user.id), "token": notification_token.token})