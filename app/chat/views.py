from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .config import chat_service
from .serializer import AddChatMessageSerializer
from .models import ChatTable
from app.user.models import UserAccountTableData
from core.chat.dto import AddMessageDto

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
            message_type=request.validated_data['message_type']
        )
        message = chat_service.add_message(dto)
        return success_response(message.model_dump())


class AdminChatView(APIView):
    @validate(AddChatMessageSerializer)
    def post(self, request: AddChatMessageSerializer) -> Response:
        chat = ChatTable.objects.get(user__id=request.validated_data['user_id'])
        user = UserAccountTableData.objects.get(phone_number="0987654321")
        dto = AddMessageDto(
            chat_id=str(chat.id),
            sender_id=str(user.id),
            content=request.validated_data['content'],
            message_type=request.validated_data['message_type']
        )
        print(dto)
        message = chat_service.add_message(dto)
        return success_response(message.model_dump())