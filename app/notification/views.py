from .models import UserNotificationToken, NotificationTable
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .serializer import AddNotificationTokenSerializer, NotificationSerializer, NotificationFilterSerializer
from core.common.values import GuayaquilDatetime
from app.user.models import UserAccountTableData
from core.common.notification import NotificationMessage
from .config import notification_service
from django.db.models import Q
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
        if request.GET.get('id'):
            notification = NotificationTable.objects.get(id=request.GET['id'])
            return success_response({
                "id": notification.id,
                "title": notification.title,
                "body": notification.body,
                "created_at": GuayaquilDatetime.localize(notification.created_at).isoformat(),
                "to": notification.to,
                "type": notification.type,
                "publish_date": GuayaquilDatetime.localize(notification.publish_date).isoformat() if notification.publish_date else None
            })
        notifications = NotificationTable.objects.all()
        return success_response([
            {
                "id": notification.id,
                "title": notification.title,
                "body": notification.body,
                "created_at": GuayaquilDatetime.localize(notification.created_at).isoformat(),
                "to": notification.to,
                "type": notification.type,
                "publish_date": GuayaquilDatetime.localize(notification.publish_date).isoformat() if notification.publish_date else None
            } for notification in notifications
        ])
    
    @validate(NotificationSerializer)
    def post(self, request: NotificationSerializer) -> Response:
        publish_date = request.validated_data.get('publish_date', None)
        created_at = GuayaquilDatetime.now()
        if publish_date:
            publish_date = GuayaquilDatetime.localize(publish_date)
        else:
            publish_date = created_at
        notification = NotificationTable.objects.create(
            title=request.validated_data['title'],
            body=request.validated_data['body'],
            created_at=created_at,
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
            "created_at": GuayaquilDatetime.localize(notification.created_at).isoformat(),
            "to": notification.to,
            "type": notification.type,
            "publish_date": GuayaquilDatetime.localize(notification.publish_date).isoformat() if notification.publish_date else None
        })
    

class NotificationFilterView(APIView):
    @validate(NotificationFilterSerializer)
    def post(self, request: NotificationFilterSerializer) -> Response:
        filters = self.build_filter(request)
        limit = request.validated_data.get('limit')
        offset = request.validated_data.get('offset')
        only_count = request.validated_data.get('only_count', False)
        total_count = NotificationTable.objects.count()
        notifications = NotificationTable.objects.filter(filters)
        total_filtered = notifications.count()
        if only_count:
            return success_response({"count": total_count, "filtered_count": total_filtered, "notifications": []})
        if limit is not None and offset is not None:
            notifications = notifications[offset:offset + limit]
        elif limit is not None:
            notifications = notifications[:limit]
        elif offset is not None:
            notifications = notifications[offset:]
        return success_response({
            "count": total_count,
            "filtered_count": total_filtered,
            "notifications": [
                {
                    "id": notification.id,
                    "title": notification.title,
                    "body": notification.body,
                    "created_at": GuayaquilDatetime.localize(notification.created_at).isoformat(),
                    "to": notification.to,
                    "type": notification.type,
                    "publish_date": GuayaquilDatetime.localize(notification.publish_date).isoformat() if notification.publish_date else None
                } for notification in notifications
            ]
        })
        
    
    def build_filter(self, data: NotificationFilterSerializer) -> Q:
        filters = Q()
        start_date = data.validated_data.get('start_date')
        end_date = data.validated_data.get('end_date')
        if data.validated_data.get('title'):
            filters &= Q(title__icontains=data.validated_data['title'])
        if data.validated_data.get('type'):
            filters &= Q(type=data.validated_data['type'])
        if start_date:
            filters &= Q(created_at__gte=start_date)
        if end_date:
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
            filters &= Q(created_at__lte= end_date)
        return filters