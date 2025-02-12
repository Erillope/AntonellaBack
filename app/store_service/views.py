from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .config import store_services
from .serializer import (CreateStoreSerializer, UpdateStoreSerializer,
                         FilterStoreServiceSerializer, AddImageToStoreSerializer)

class StoreServiceView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        store_service = store_services.find(request.GET.get('id'))
        return success_response(store_service.model_dump())
    
    @validate(CreateStoreSerializer)
    def post(self, request: CreateStoreSerializer) -> Response:
        store_service = store_services.create(request.to_dto())
        return success_response(store_service.model_dump())
    
    @validate(UpdateStoreSerializer)
    def put(self, request: UpdateStoreSerializer) -> Response:
        store_service = store_services.update(request.to_dto())
        return success_response(store_service.model_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        store_service = store_services.delete(request.GET.get('id'))
        return success_response(store_service.model_dump())


class StoreServiceFilterView(APIView):
    def get(self, request: Request) -> Response:
        filter_serializer = FilterStoreServiceSerializer(data=request.GET)
        filter_serializer.is_valid(raise_exception=True)
        store_services = store_services.filter(filter_serializer.to_dto())
        return success_response([store_service.model_dump() for store_service in store_services])


class StoreServiceImageView(APIView):
    @validate(AddImageToStoreSerializer)
    def post(self, request: AddImageToStoreSerializer) -> Response:
        store_service = store_services.add_image(**request.validated_data)
        return success_response(store_service.model_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        store_service = store_services.delete_image(request.GET.get('store_service_id'), request.GET.get('image'))
        return success_response(store_service.model_dump())