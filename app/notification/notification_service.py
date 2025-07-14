from core.common.notification import NotificationService, NotificationMessage
import firebase_admin #type: ignore
from firebase_admin import credentials, messaging
from .models import UserNotificationToken
from core.common.config import resources_path
import os

class FirebaseNotificationService(NotificationService):
    def __init__(self) -> None:
        credential_path = os.path.join(resources_path, 'antonella_firebase.json')
        cred = credentials.Certificate(credential_path)
        firebase_admin.initialize_app(cred)
    
    def send_notification(self, message: NotificationMessage) -> None:
        message = messaging.Message(
            notification=messaging.Notification(
                title=message.title,
                body=message.body,
            ),
            token=UserNotificationToken.objects.get(user__id=message.user_id).token,
        )
        messaging.send(message)