from core.common.notification import NotificationService, NotificationMessage, NotificationType
import firebase_admin #type: ignore
from firebase_admin import credentials, messaging
from .models import UserNotificationToken
from core.common.config import resources_path
import os
from apscheduler.schedulers.background import BackgroundScheduler #type: ignore

class FirebaseNotificationService(NotificationService):
    def __init__(self) -> None:
        credential_path = os.path.join(resources_path, 'antonella_firebase.json')
        cred = credentials.Certificate(credential_path)
        firebase_admin.initialize_app(cred)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
    
    def send_notification(self, message_data: NotificationMessage) -> None:
        if not UserNotificationToken.objects.filter(user__id=message_data.user_id).exists(): return
        message = messaging.Message(
            notification=messaging.Notification(
                title=message_data.title,
                body=message_data.body,
            ),
            token=UserNotificationToken.objects.get(user__id=message_data.user_id).token,
        )
        if message_data.type == NotificationType.PROGRAMADA and message_data.publish_date:
            self.scheduler.add_job(lambda: messaging.send(message), 'date', run_date=message_data.publish_date)
        else:
            messaging.send(message)