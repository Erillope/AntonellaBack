from .repository import DjangoChatMessageSaved, DjangoGetChatMessage
from core.chat.chat_service import ChatService
from app.notification.notification_service import FirebaseNotificationService

notification_service = FirebaseNotificationService()

get_chat_message = DjangoGetChatMessage()

save_chat_message = DjangoChatMessageSaved()

chat_service = ChatService(get_chat_message)