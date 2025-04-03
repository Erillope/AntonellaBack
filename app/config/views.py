from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from core.common.config import AppConfig


class CategoriesApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        categories_info = AppConfig.categories_subtypes()
        return success_response(categories_info)


class ProductTypesApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        product_types = AppConfig.producy_types()
        return success_response(product_types)