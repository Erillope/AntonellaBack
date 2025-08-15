from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .config import order_service, service_item_service, product_item_service
from .serializer import (CreateOrderSerializer, UpdateOrderSerializer, ServiceItemSerializer, UpdateServiceItemSerializer,
                         ProductItemSerializer, UpdateProductItemSerializer, FilterServiceItemBySerializer,
                         RequestEmployeeServiceInfoSerializer, FilterOrderSerializer)

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


class FilterOrderApiView(APIView):
    @validate(FilterOrderSerializer)
    def post(self, request: FilterOrderSerializer) -> Response:
        filter_dto = request.to_dto()
        filter_data = order_service.filter_orders(filter_dto)
        return success_response(filter_data.model_dump())

class ServiceItemApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        if request.GET.get('id'):
            service_item = service_item_service.get(request.GET.get('id'))
            return success_response(service_item.model_dump())
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


class ProductItemApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        order_id = request.GET.get('order_id')
        product_items = product_item_service.get_product_items(order_id)
        return success_response([item.model_dump() for item in product_items])
    
    @validate(ProductItemSerializer)
    def post(self, request: ProductItemSerializer) -> Response:
        product_item = product_item_service.create_product_item(request.to_dto(), request.data['order_id'])
        return success_response(product_item.model_dump())
    
    @validate(UpdateProductItemSerializer)
    def put(self, request: UpdateProductItemSerializer) -> Response:
        product_item = product_item_service.update_product_item(request.to_dto())
        return success_response(product_item.model_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        product_item_service.delete_product_item(request.GET.get('id'))
        return success_response({"message": "Product item deleted successfully"})


class ServiceItemFilterApiView(APIView):
    @validate(FilterServiceItemBySerializer)
    def post(self, request: FilterServiceItemBySerializer) -> Response:
        filter_dto = request.to_dto()
        service_items = service_item_service.filter_service_items(filter_dto)
        return success_response(service_items.model_dump())


class EmployeeServiceInfoView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        employee_id = request.GET.get('employee_id')
        if not employee_id:
            return Response({"error": "Employee ID is required"}, status=400)

        service_info = service_item_service.get_employee_calendar(employee_id)
        return success_response([item.model_dump() for item in service_info])

    @validate(RequestEmployeeServiceInfoSerializer)
    def post(self, request: RequestEmployeeServiceInfoSerializer) -> Response:
        employee_service_info = service_item_service.get_employee_service_info(request.to_dto())
        return success_response(employee_service_info.model_dump())