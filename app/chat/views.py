from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .config import chat_service
from app.notification.config import NotificationConfig
from core.common.notification import NotificationMessage
from .serializer import AddChatMessageSerializer
from .models import ChatTable, ChatMessageTable
from app.user.models import UserAccountTableData
from core.chat.dto import AddMessageDto
from core.chat.chat import MessageType

class ChatApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        user_id = request.GET.get('user_id')
        offset = int(request.GET.get('offset')) if request.GET.get('offset') else 0
        limit = int(request.GET.get('limit')) if request.GET.get('limit') else 20
        if user_id:
            chats = chat_service.get_messages(user_id, offset, limit)
            return success_response([chat.model_dump() for chat in chats])
        return success_response([
            {
                "id": chat.id,
                "user_id": chat.user.id
            }
            for chat in ChatTable.objects.all()
        ])


class UserChatView(APIView):
    @validate(AddChatMessageSerializer)
    def post(self, request: AddChatMessageSerializer) -> Response:
        chat = ChatTable.objects.get(user__id=request.validated_data['user_id'])
        dto = AddMessageDto(
            chat_id=str(chat.id),
            sender_id=str(request.validated_data['user_id']),
            content=request.validated_data['content'],
            message_type=request.validated_data['message_type'],
            readed_by_client=True,
            readed_by_admin=False
        )
        message = chat_service.add_message(dto)
        return success_response(message.model_dump())
    
    @validate()
    def put(self, request: Request) -> Response:
        message_id = request.GET.get('message_id')
        message = ChatMessageTable.objects.get(id=message_id)
        message.readed_by_client = True
        message.save()
        return success_response({"message": "Message marked as read by client"})


class AdminChatView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        chats = chat_service.get_user_chats()
        return success_response([chat.model_dump() for chat in chats])
    
    @validate(AddChatMessageSerializer)
    def post(self, request: AddChatMessageSerializer) -> Response:
        chat = ChatTable.objects.get(user__id=request.validated_data['user_id'])
        user = UserAccountTableData.objects.get(phone_number="0987654321")
        dto = AddMessageDto(
            chat_id=str(chat.id),
            sender_id=str(user.id),
            content=request.validated_data['content'],
            message_type=request.validated_data['message_type'],
            readed_by_client=False,
            readed_by_admin=True
        )
        message = chat_service.add_message(dto)
        notification_message = NotificationMessage(
            title="Nuevo mensaje de Antonella",
            body=message.content if message.message_type == MessageType.TEXT else "Antonella te ha enviado una foto",
            user_id=str(chat.user.id),
            redirect_to='CHAT',
        )
        NotificationConfig.notification_service.send_notification(notification_message)
        return success_response(message.model_dump())
    
    @validate()
    def put(self, request: Request) -> Response:
        message_id = request.GET.get('message_id')
        message = ChatMessageTable.objects.get(id=message_id)
        message.readed_by_admin = True
        message.save()
        return success_response({"message": "Message marked as read by admin"})