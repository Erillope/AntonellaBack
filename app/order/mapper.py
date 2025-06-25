from ..common.table_mapper import TableMapper
from core.order.domain.order import Order, OrderFactory
from core.order.domain.item import ServiceItem, ServiceItemFactory, ProductItem, ProductItemFactory
from core.order.domain.values import OrderStatusInfo, OrderStatus, PaymentStatus, PaymentType, Progresstatus, DateInfo, Price, Payment
from .models import OrderTable, ServiceItemTable, PaymentTable, ProductItemTable

class OrderTableMapper(TableMapper[OrderTable, Order]):
    def to_model(self, table: OrderTable) -> Order:
        return OrderFactory.load(
            id=str(table.id),
            client_id=str(table.client.id),
            status=OrderStatusInfo(
                status=OrderStatus(table.status.upper()),
                progress_status=Progresstatus(table.progress_status.upper()),
                payment_status=PaymentStatus(table.payment_status.upper()),
                payment_type=PaymentType(table.payment_type.upper()),
                client_confirmed=table.client_confirmed.upper()
            ),
            card_charge=table.card_charge,
            created_date=table.created_date
        )
    
    def to_table(self, model: Order) -> OrderTable:
        return OrderTable(
            id=model.id,
            client_id=model.client_id,
            status=model.status.status.lower(),
            progress_status=model.status.progress_status.lower(),
            payment_status=model.status.payment_status.lower(),
            payment_type=model.status.payment_type.lower(),
            client_confirmed=model.status.client_confirmed.lower(),
            created_date=model.created_date,
            card_charge=model.card_charge,
        )


class ServiceItemTableMapper(TableMapper[ServiceItemTable, ServiceItem]):
    def to_table(self, model: ServiceItem) -> ServiceItemTable:
        return ServiceItemTable(
            id=model.id,
            order_id=model.get_order_id(),
            service_id=model.service_id,
            payment_percentage=model.payment_percentage,
            date_info_day=model.date_info.day,
            date_info_start_time=model.date_info.start_time,
            date_info_end_time=model.date_info.end_time,
            status=model.status.lower(),
            base_price=model.price.base_price if model.price else None
        )
    
    def to_model(self, table: ServiceItemTable) -> ServiceItem:
        return ServiceItemFactory.load(
            id=str(table.id),
            service_id=str(table.service_id),
            order_id=str(table.order_id),
            day= DateInfo(
                day=table.date_info_day,
                start_time=table.date_info_start_time,
                end_time=table.date_info_end_time
            ),
            status=Progresstatus(table.status.upper()),
            price=Price.calculate(table.base_price) if table.base_price else None,
            payment_percentage=table.payment_percentage,
            payments=[
                Payment(
                    employee_id=str(payment.employee_id),
                    percentage=payment.percentage,
                    amount=payment.amount
                ) for payment in PaymentTable.from_service_item(table.id)
            ],
        )


class ProductItemTableMapper(TableMapper[ProductItemTable, ProductItem]):
    def to_table(self, model: ProductItem) -> ProductItemTable:
        return ProductItemTable(
            id=model.id,
            order_id=model.get_order_id(),
            product_id=model.product_id,
            quantity=model.quantity,
            base_price=model.price.base_price
        )
    
    def to_model(self, table: ProductItemTable) -> ProductItem:
        return ProductItemFactory.load(
            id=str(table.id),
            order_id=str(table.order_id),
            product_id=str(table.product_id),
            quantity=table.quantity,
            price=Price.calculate(table.base_price)
        )