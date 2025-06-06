from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .config import order_service, service_item_service
from .serializer import *

class OrderApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        if request.GET.get('id'):
            order = order_service.get_order(request.GET.get('id'))
            return success_response(order.model_dump())
        else:
            orders = order_service.get_all()
            return success_response([order.model_dump() for order in orders])
    
    @validate(CreateOrderSerializer)
    def post(self, request: CreateOrderSerializer) -> Response:
        order = order_service.create_order(request.to_dto())
        return success_response(order.model_dump())
    
    @validate(UpdateOrderSerializer)
    def put(self, request: UpdateOrderSerializer) -> Response:
        order = order_service.update_order(request.to_dto())
        return success_response(order.model_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        order_service.delete_order(request.GET.get('id'))
        return success_response({"message": "Order deleted successfully"})
    

class ServiceItemApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        order_id = request.GET.get('order_id')
        service_items = service_item_service.get_service_items(order_id)
        return success_response([item.model_dump() for item in service_items])
    
    @validate(ServiceItemSerializer)
    def post(self, request: ServiceItemSerializer) -> Response:
        service_item = service_item_service.create_service_item(request.to_dto(), request.data['order_id'])
        return success_response(service_item.model_dump())
    
    @validate(UpdateServiceItemSerializer)
    def put(self, request: UpdateServiceItemSerializer) -> Response:
        service_item = service_item_service.update_service_item(request.to_dto())
        return success_response(service_item.model_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        service_item_service.delete_service_item(request.GET.get('id'))
        return success_response({"message": "Service item deleted successfully"})