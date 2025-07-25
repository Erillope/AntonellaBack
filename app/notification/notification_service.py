from core.common.notification import NotificationService, NotificationMessage, NotificationType
import firebase_admin #type: ignore
from firebase_admin import credentials, messaging
from .models import UserNotificationToken
from core.common.config import resources_path
import os
from firebase_admin._messaging_utils import UnregisteredError #type: ignore

class FirebaseNotificationService(NotificationService):
    def __init__(self) -> None:
        if not firebase_admin._apps:
            credential_path = os.path.join(resources_path, 'antonella_firebase.json')
            cred = credentials.Certificate(credential_path)
            firebase_admin.initialize_app(cred)
    
    def send_notification(self, message_data: NotificationMessage) -> None:
        if not UserNotificationToken.objects.filter(user__id=message_data.user_id).exists(): return
        message = messaging.Message(
            notification=messaging.Notification(
                title=message_data.title,
                body=message_data.body,
            ),
            data={
                'redirect_to': message_data.redirect_to,
                'notification_type': message_data.notification_type,
            },
            token=UserNotificationToken.objects.get(user__id=message_data.user_id).token,
        )
        if message_data.type == NotificationType.PROGRAMADA and message_data.publish_date:
            pass
            #self.scheduler.add_job(lambda: self.send(message), 'date', run_date=message_data.publish_date)
        else:
            self.send(message)
    
    def send(self, message: messaging.Message) -> None:
        try:
            messaging.send(message)
        except UnregisteredError:
            print("Token no registrado o caducado.")