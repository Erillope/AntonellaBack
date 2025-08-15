from .dto import CreateOrderDto, ServiceItemDto, OrderDto, PaymentDto, ProductItemDto
from ..domain import OrderFactory, ServiceItem, ServiceItemFactory, Payment, Order, ProductItem, ProductItemFactory

class OrderMapper:
    @classmethod
    def to_order(cls, dto: CreateOrderDto) -> Order:
        return OrderFactory.create(
            client_id=dto.client_id,
            status=dto.status,
            iva=dto.iva
        )
    
    @classmethod
    def to_order_dto(cls, order: Order) -> OrderDto:
        return OrderDto(
            id=order.id,
            client_id=order.client_id,
            status=order.status,
            created_date=order.created_date,
            order_date=order.order_date,
            card_charge=order.card_charge,
            iva=order.iva
        )


class ServiceItemMapper:
    @classmethod
    def to_service_item(cls, dto: ServiceItemDto) -> ServiceItem:
        p = [Payment(employee_id=payment.employee_id) for payment in dto.payments]
        if dto.payment_percentage and dto.base_price:
            p = [
                Payment.calculate(
                    employee_id=payment.employee_id,
                    base_price=dto.base_price*dto.payment_percentage,
                    percentage=payment.percentage
                )     
                for payment in dto.payments if payment.percentage is not None
            ]
        return ServiceItemFactory.create(
            service_id=dto.service_id,
            day=dto.date_info.day,
            start_time=dto.date_info.start_time,
            base_price=dto.base_price,
            payments=p,
        )
    
    @classmethod
    def to_service_item_dto(cls, item: ServiceItem) -> ServiceItemDto:
        return ServiceItemDto(
            id=item.id,
            order_id=item.get_order_id(),
            service_id=item.service_id,
            payment_percentage=item.payment_percentage,
            date_info=item.date_info,
            status=item.status,
            base_price=item.price.base_price if item.price else None,
            payments=[
                PaymentDto(
                    employee_id=payment.employee_id,
                    percentage=payment.percentage
                ) for payment in item.payments
            ]
        )


class ProductItemMapper:
    @classmethod
    def to_product_item(cls, dto: ProductItemDto) -> ProductItem:
        return ProductItemFactory.create(
            product_id=dto.product_id,
            quantity=dto.quantity,
            base_price=dto.base_price,
        )
    
    @classmethod
    def to_product_item_dto(cls, item: ProductItem) -> ProductItemDto:
        return ProductItemDto(
            id=item.id,
            order_id=item.get_order_id(),
            product_id=item.product_id,
            quantity=item.quantity,
            base_price=item.price.base_price,
        )