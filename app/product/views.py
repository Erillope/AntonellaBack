from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .config import product_service
from .serializer import CreateProductSerializer, UpdateProductSerializer

class ProductApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        if request.GET.get('id'):
            product = product_service.get(request.GET.get('id'))
            return success_response(product.model_dump())
        else:
            products = product_service.get_all()
            return success_response([product.model_dump() for product in products])
    
    @validate(CreateProductSerializer)
    def post(self, request: CreateProductSerializer) -> Response:
        product = product_service.create(request.to_dto())
        return success_response(product.model_dump())
    
    @validate(UpdateProductSerializer)
    def put(self, request: UpdateProductSerializer) -> Response:
        product = product_service.update(request.to_dto())
        return success_response(product.model_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        product = product_service.delete(request.GET.get('id'))
        return success_response(product.model_dump())