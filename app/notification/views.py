from .models import UserNotificationToken, NotificationTable
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .serializer import AddNotificationTokenSerializer, NotificationSerializer
from core.common.values import GuayaquilDatetime
from app.user.models import UserAccountTableData
from core.common.notification import NotificationMessage
from .config import notification_service
from datetime import datetime

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


class NotificationView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        notifications = NotificationTable.objects.all()
        return success_response([
            {
                "id": notification.id,
                "title": notification.title,
                "body": notification.body,
                "created_at": notification.created_at.isoformat(),
                "to": notification.to
            } for notification in notifications
        ])
    
    @validate(NotificationSerializer)
    def post(self, request: NotificationSerializer) -> Response:
        publish_date = request.validated_data.get('publish_date', None)
        if publish_date:
            publish_date = GuayaquilDatetime.localize(publish_date)
        notification = NotificationTable.objects.create(
            title=request.validated_data['title'],
            body=request.validated_data['body'],
            created_at=GuayaquilDatetime.now(),
            to=request.validated_data['to'],
            type=request.validated_data['type'],
            publish_date=publish_date
        )
        for user in UserAccountTableData.objects.all():
            if UserNotificationToken.objects.filter(user=user).exists():
                notification_service.send_notification(
                    NotificationMessage(
                        user_id=str(user.id),
                        title=notification.title,
                        body=notification.body,
                        type=notification.type,
                        publish_date=notification.publish_date if notification.publish_date else None
                    )
                )
        
        return success_response({
            "id": notification.id,
            "title": notification.title,
            "body": notification.body,
            "created_at": notification.created_at.isoformat(),
            "to": notification.to,
            "type": notification.type.value,
            "publish_date": notification.publish_date.isoformat() if notification.publish_date else None
        })