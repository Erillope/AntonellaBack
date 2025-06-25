from rest_framework import serializers
from core.order.domain.values import Progresstatus, OrderStatus, PaymentStatus, PaymentType, DateInfo, OrderStatusInfo
from core.order.service.dto import CreateOrderDto, UpdateOrderDto, RequestEmployeeScheduleDto, ServiceItemDto, PaymentDto, UpdateServiceItemDto, ProductItemDto, UpdateProductItemDto, FilterServiceItemByDto, RequestEmployeeServiceInfoDto
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
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
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
            base_price=self.validated_data.get('base_price'),
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
            id=str(self.validated_data['id']),
            service_id=str(self.validated_data.get('service_id')) if 'service_id' in self.validated_data else None,
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
    client_confirmed = serializers.ChoiceField(choices=[(status.value, status.value) for status in OrderStatus])
    
    def to_order_status_info(self) -> OrderStatusInfo:
        return OrderStatusInfo(
            status=OrderStatus(self.validated_data['status']),
            progress_status=Progresstatus(self.validated_data['progress_status']),
            payment_status=PaymentStatus(self.validated_data['payment_status']),
            payment_type=PaymentType(self.validated_data['payment_type']),
            client_confirmed=self.validated_data['client_confirmed']
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
    status = serializers.ChoiceField(choices=[(status.value, status.value) for status in OrderStatus], required=False)
    progress_status = serializers.ChoiceField(choices=[(status.value, status.value) for status in Progresstatus], required=False)
    payment_status = serializers.ChoiceField(choices=[(status.value, status.value) for status in PaymentStatus], required=False)
    payment_type = serializers.ChoiceField(choices=[(ptype.value, ptype.value) for ptype in PaymentType], required=False)
    client_confirmed = serializers.ChoiceField(choices=[(status.value, status.value) for status in OrderStatus], required=False)
    
    def to_dto(self) -> UpdateOrderDto:
        return UpdateOrderDto(
            id=str(self.validated_data['id']),
            client_id=str(self.validated_data.get('client_id')) if 'client_id' in self.validated_data else None,
            status= self.validated_data.get('status'),
            progress_status=self.validated_data.get('progress_status'),
            payment_status=self.validated_data.get('payment_status'),
            payment_type=self.validated_data.get('payment_type'),
            client_confirmed=self.validated_data.get('client_confirmed')
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

class ProductItemSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def to_dto(self) -> ProductItemDto:
        return ProductItemDto(
            order_id=str(self.validated_data['order_id']),
            product_id=str(self.validated_data['product_id']),
            quantity=self.validated_data['quantity'],
            base_price=self.validated_data['base_price']
        )


class UpdateProductItemSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    product_id = serializers.UUIDField(required=False)
    quantity = serializers.IntegerField(required=False)
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    
    def to_dto(self) -> UpdateProductItemDto:
        return UpdateProductItemDto(
            id=self.validated_data['id'],
            product_id=self.validated_data.get('product_id'),
            quantity=self.validated_data.get('quantity'),
            base_price=self.validated_data.get('base_price')
        )


class FilterServiceItemBySerializer(serializers.Serializer):
    client_id = serializers.UUIDField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    status = serializers.ChoiceField(choices=[(status.value, status.value) for status in Progresstatus], required=False)
    service_id = serializers.UUIDField(required=False)
    employee_id = serializers.UUIDField(required=False)
    limit = serializers.IntegerField(required=False)
    offset = serializers.IntegerField(required=False)
    
    def to_dto(self) -> FilterServiceItemByDto:
        return FilterServiceItemByDto(
            client_id=str(self.validated_data.get('client_id')) if self.validated_data.get('client_id') else None,
            start_date=self.validated_data.get('start_date'),
            end_date=self.validated_data.get('end_date'),
            status=self.validated_data.get('status'),
            service_id=str(self.validated_data.get('service_id')) if self.validated_data.get('service_id') else None,
            employee_id=str(self.validated_data.get('employee_id')) if self.validated_data.get('employee_id') else None,
            limit=self.validated_data.get('limit'),
            offset=self.validated_data.get('offset')
        )


class RequestEmployeeServiceInfoSerializer(serializers.Serializer):
    employee_id = serializers.UUIDField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    limit = serializers.IntegerField(required=False)
    offset = serializers.IntegerField(required=False)
    
    def to_dto(self) -> RequestEmployeeServiceInfoDto:
        return RequestEmployeeServiceInfoDto(
            employee_id=str(self.validated_data['employee_id']),
            start_date=self.validated_data['start_date'],
            end_date=self.validated_data['end_date'],
            limit=self.validated_data.get('limit'),
            offset=self.validated_data.get('offset')
        )