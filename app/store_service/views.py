from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .config import store_services, question_service
from .serializer import (CreateStoreSerializer, UpdateStoreSerializer, CreateQuestionSerializer,          UpdateQuestion)

class StoreServiceView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        store_service = store_services.find(request.GET.get('id'))
        return success_response(store_service.service_dump())
    
    @validate(CreateStoreSerializer)
    def post(self, request: CreateStoreSerializer) -> Response:
        store_service = store_services.create(request.to_dto())
        return success_response(store_service.service_dump())
    
    @validate(UpdateStoreSerializer)
    def put(self, request: UpdateStoreSerializer) -> Response:
        store_service = store_services.update(request.to_dto())
        return success_response(store_service.service_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        store_service = store_services.delete(request.GET.get('id'))
        return success_response(store_service.service_dump())


class QuestionView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        question = question_service.find(request.GET.get('id'))
        return success_response(question.question_dump())
    
    @validate(CreateQuestionSerializer)
    def post(self, request: CreateQuestionSerializer) -> Response:
        question = question_service.create(request.validated_data['service_id'], request.to_dto())
        return success_response(question.question_dump())
    
    @validate(UpdateQuestion)
    def put(self, request: UpdateQuestion) -> Response:
        question = question_service.update(request.to_dto())
        return success_response(question.question_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        question = question_service.delete(request.GET.get('id'))
        return success_response(question.question_dump())