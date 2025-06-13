from rest_framework import serializers
from core.order.domain.values import Progresstatus, OrderStatus, PaymentStatus, PaymentType, DateInfo, OrderStatusInfo
from core.order.service.dto import CreateOrderDto, UpdateOrderDto, RequestEmployeeScheduleDto, ServiceItemDto, PaymentDto, UpdateServiceItemDto
from typing import List

class DateInfoSerializer(serializers.Serializer):
    day = serializers.DateField()
    start = serializers.TimeField()
    end = serializers.TimeField(required=False)
    
    def to_date_info(self) -> DateInfo:
        return DateInfo(
            day=self.validated_data['day'],
            start_time=self.validated_data['start'],
            end_time=self.validated_data.get('end')
        )


class PaymentSerializer(serializers.Serializer):
    employee_id = serializers.UUIDField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    
    def to_payment(self) -> PaymentDto:
        return PaymentDto(
            employee_id=str(self.validated_data['employee_id']),
            percentage=self.validated_data.get('percentage'),
        )
    
    
class ServiceItemSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    service_id = serializers.UUIDField()
    date_info = DateInfoSerializer()
    status = serializers.ChoiceField(choices=[(status.value, status.value) for status in Progresstatus])
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    payments = serializers.ListField(child=PaymentSerializer())
    payment_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    
    def to_dto(self) -> ServiceItemDto:
        date_info = DateInfoSerializer(data=self.validated_data['date_info'])
        date_info.is_valid()
        payments: List[PaymentDto] = []
        for payment_data in self.validated_data.get('payments', []):
            payment = PaymentSerializer(data=payment_data)
            payment.is_valid()
            payments.append(payment.to_payment())
            
        return ServiceItemDto(
            order_id = str(self.validated_data['order_id']),
            service_id=str(self.validated_data['service_id']),
            payment_percentage=self.validated_data.get('payment_percentage'),
            date_info=date_info.to_date_info(),
            status=Progresstatus(self.validated_data['status']),
            base_price=self.validated_data['base_price'],
            payments=payments
        )


class UpdateServiceItemSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    service_id = serializers.UUIDField(required=False)
    payment_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    date_info = DateInfoSerializer(required=False)
    status = serializers.ChoiceField(choices=[(status.value, status.value) for status in Progresstatus], required=False)
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    payments = serializers.ListField(child=PaymentSerializer(), required=False)
    
    def to_dto(self) -> UpdateServiceItemDto:
        date_info = DateInfoSerializer(data=self.validated_data['date_info']) if 'date_info' in self.validated_data else None
        if date_info: date_info.is_valid()
        payments: List[PaymentDto] = []
        for payment_data in self.validated_data.get('payments', []):
            payment = PaymentSerializer(data=payment_data)
            payment.is_valid()
            payments.append(payment.to_payment())
            
        return UpdateServiceItemDto(
            id=self.validated_data['id'],
            service_id=self.validated_data.get('service_id'),
            payment_percentage=self.validated_data.get('payment_percentage'),
            date_info=date_info,
            status=Progresstatus(self.validated_data['status']) if 'status' in self.validated_data else None,
            base_price=self.validated_data.get('base_price'),
            payments=payments
        )


class OrderStatusInfoSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[(status.value, status.value) for status in OrderStatus])
    progress_status = serializers.ChoiceField(choices=[(status.value, status.value) for status in Progresstatus])
    payment_status = serializers.ChoiceField(choices=[(status.value, status.value) for status in PaymentStatus])
    payment_type = serializers.ChoiceField(choices=[(ptype.value, ptype.value) for ptype in PaymentType])
    
    def to_order_status_info(self) -> OrderStatusInfo:
        return OrderStatusInfo(
            status=OrderStatus(self.validated_data['status']),
            progress_status=Progresstatus(self.validated_data['progress_status']),
            payment_status=PaymentStatus(self.validated_data['payment_status']),
            payment_type=PaymentType(self.validated_data['payment_type'])
        )
    
class CreateOrderSerializer(serializers.Serializer):
    client_id = serializers.UUIDField()
    status = OrderStatusInfoSerializer()
    
    def to_dto(self) -> CreateOrderDto:
        status_info = OrderStatusInfoSerializer(data=self.validated_data['status'])
        status_info.is_valid()
        return CreateOrderDto(
            client_id=str(self.validated_data['client_id']),
            status=status_info.to_order_status_info()
        )

class UpdateOrderSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    client_id = serializers.UUIDField(required=False)
    status = OrderStatusInfoSerializer(required=False)
    
    def to_dto(self) -> UpdateOrderDto:
        status_info = OrderStatusInfoSerializer(**self.validated_data['status']) if 'status' in self.validated_data else None
        if status_info: status_info.validate()
        return UpdateOrderDto(
            id=self.validated_data['id'],
            client_id=self.validated_data.get('client_id'),
            status=status_info.to_order_status_info() if status_info else None
        )


class RequestEmployeeScheduleSerializer(serializers.Serializer):
    employee_id = serializers.UUIDField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    
    def to_dto(self) -> RequestEmployeeScheduleDto:
        return RequestEmployeeScheduleDto(
            employee_id=self.validated_data['employee_id'],
            start_date=self.validated_data['start_date'],
            end_date=self.validated_data['end_date']
        )