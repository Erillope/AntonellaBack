from .dto import CreateOrderDto, ServiceItemDto, OrderDto, PaymentDto
from ..domain import OrderFactory, ServiceItem, ServiceItemFactory, Payment, Order

class OrderMapper:
    @classmethod
    def to_order(cls, dto: CreateOrderDto) -> Order:
        return OrderFactory.create(
            client_id=dto.client_id,
            status=dto.status,
        )
    
    @classmethod
    def to_order_dto(cls, order: Order) -> OrderDto:
        return OrderDto(
            id=order.id,
            client_id=order.client_id,
            status=order.status
        )


class ServiceItemMapper:
    @classmethod
    def to_service_item(cls, dto: ServiceItemDto) -> ServiceItem:
        return ServiceItemFactory.create(
            service_id=dto.service_id,
            day=dto.date_info.day,
            start_time=dto.date_info.start_time,
            base_price=dto.base_price,
            payments=[
                Payment.calculate(
                    employee_id=payment.employee_id,
                    base_price=dto.base_price,
                    percentage=payment.percentage
                )     
                for payment in dto.payments if payment.percentage is not None
            ]
        )
    
    @classmethod
    def to_service_item_dto(cls, item: ServiceItem) -> ServiceItemDto:
        return ServiceItemDto(
            order_id=item.get_order_id(),
            service_id=item.service_id,
            payment_percentage=item.payment_percentage,
            date_info=item.date_info,
            status=item.status,
            base_price=item.price.base_price,
            payments=[
                PaymentDto(
                    employee_id=payment.employee_id,
                    percentage=payment.percentage
                ) for payment in item.payments
            ]
        )