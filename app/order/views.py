from typing import Any, Dict
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from core.order.domain.values import Progresstatus
from .config import order_service, service_item_service, product_item_service
from .serializer import (CreateOrderSerializer, UpdateOrderSerializer, ServiceItemSerializer, UpdateServiceItemSerializer,
                         ProductItemSerializer, UpdateProductItemSerializer, FilterServiceItemBySerializer,
                         RequestEmployeeServiceInfoSerializer, FilterOrderSerializer, ServiceItemProgressSerializer,
                         EmployeePaymentSerializer, EmployeePaymentFilterSerializer)
from core.order.service.dto import UpdateServiceItemDto
from app.notification.config import NotificationConfig
from core.common.notification import NotificationMessage
from .models import EmployeePaymentTable
from django.db.models import Q

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


class ServiceItemProgressApiView(APIView):
    @validate(ServiceItemProgressSerializer)
    def post(self, request: ServiceItemProgressSerializer) -> Response:
        data = request.validated_data
        service_item = service_item_service.update_service_item(
            UpdateServiceItemDto(
                id=data['id'],
                status=Progresstatus(data['status'])
            )
        )
        order = order_service.get_order(service_item.order_id)
        status = service_item.status
        if status == Progresstatus.IN_PROGRESS:
            NotificationConfig.notification_service.send_notification(
                NotificationMessage(
                    title="Servicio empezado",
                    body=f"El servicio ha comenzado.",
                    user_id=str(order.client_id),
                    redirect_to="servicio_progreso"
                    extra={
                        'redirect_to': "servicio_progreso",
                        "title": "Servicio empezado",
                        "body": f"El servicio ha comenzado.",
                        "user_id": str(order.client_id),
                    }
                )
            )
        if status == Progresstatus.FINISHED:
            NotificationConfig.notification_service.send_notification(
                NotificationMessage(
                    title="Servicio finalizado",
                    body=f"El servicio ha finalizado.",
                    user_id=str(order.client_id),
                    redirect_to="servicio_finalizado"
                    extra={
                        'redirect_to': "servicio_finalizado",
                        "title": "Servicio finalizado",
                        "body": f"El servicio ha finalizado.",
                        "user_id": str(order.client_id),
                    }
                )
            )
        return success_response(service_item.model_dump())


class ProductItemApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        if request.GET.get('id'):
            product_item = product_item_service.get_product_item(request.GET.get('id'))
            return success_response(product_item.model_dump())
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


class EmployeePaymentView(APIView):
    @validate(EmployeePaymentSerializer)
    def post(self, request: EmployeePaymentSerializer) -> Response:
        data = request.validated_data
        employee_payment = EmployeePaymentTable.objects.create(
            employee_id=data['employee_id'],
            amount=data['amount']
        )
        return success_response(map_employee_payment(employee_payment))


class EmployeePaymentFilterView(APIView):
    @validate(EmployeePaymentFilterSerializer)
    def post(self, request: EmployeePaymentFilterSerializer) -> Response:
        data = request.validated_data
        _filter = self._build_filter(data)
        employees = EmployeePaymentTable.objects.filter(_filter)
        total_count = EmployeePaymentTable.objects.count()
        filtered_count = employees.count()
        if data.get('offset') and data.get('limit'):
            employees = employees[data['offset']:data['offset'] + data['limit']]
        if data.get('offest'):
            employees = employees[data['offset']:]
        if data.get('limit'):
            employees = employees[:data['limit']]
        return success_response({
            'total_count': total_count,
            'filtered_count': filtered_count,
            'payments': [map_employee_payment(emp) for emp in employees]
        })

    def _build_filter(self, data: Dict[str, Any]) -> Q:
        filters = Q()
        if 'employee_name' in data:
            filters &= Q(employee__name__icontains=data['employee_name'])
        if 'start_date' in data:
            filters &= Q(created_date__gte=data['start_date'])
        if 'end_date' in data:
            filters &= Q(created_date__lte=data['end_date'])
        return filters
    
def map_employee_payment(table: EmployeePaymentTable) -> Dict[str, Any]:
    return {
        "employee_id": str(table.employee.id),
        "amount": table.amount,
        "created_date": table.created_date.isoformat()
    }