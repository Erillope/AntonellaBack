from .repository import DjangoChatMessageSaved, DjangoGetChatMessage
from core.chat.chat_service import ChatService

get_chat_message = DjangoGetChatMessage()

save_chat_message = DjangoChatMessageSaved()

chat_service = ChatService(get_chat_message)