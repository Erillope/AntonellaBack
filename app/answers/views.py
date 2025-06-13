from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .serializer import *
from .models import *
from core.common import save_storage_image, SystemException
from core.common.image_storage import Base64ImageStorage
from typing import Dict, Any

class AnswerApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        answer = AnswerTableData.objects.get(question__id=request.GET.get('question_id'))
        return success_response(answer_response(answer))

    @validate(AnswerSerializer)
    def post(self, request: AnswerSerializer) -> Response:
        data = request.validated_data
        answer : AnswerTableData
        if data['answer'].get('text'):
            answer = TextAnswerTableData.objects.create(
                client_id=data['client_id'],
                question_id=data['question_id'],
                service_item_id=data['service_item_id'],
                text=data['answer']['text']
            )
        elif data['answer'].get('images'):
            images = [Base64ImageStorage(folder='answer', base64_image=image) for image in data['answer']['images']]
            images_paths = [image.get_url() for image in images]
            for image in images:
                save_storage_image.save(image)
            answer = ImageAnswerTableData.objects.create(
                client_id=data['client_id'],
                question_id=data['question_id'],
                service_item_id=data['service_item_id'],
                images=images_paths
            )
        else:
            raise SystemException("Debe enviar una respuesta de tipo texto o imagen")
        answer.save()
        return success_response(answer_response(answer))


def answer_response(answer: AnswerTableData) -> Dict[str, Any]:
    return {
        "client_id": answer.client_id,
        "question_id": answer.question_id,
        "service_item_id": answer.service_item_id,
        "answer_type": "IMAGE" if isinstance(answer, ImageAnswerTableData) else "TEXT",
        "answer": answer.text if isinstance(answer, TextAnswerTableData) else answer.images
    }