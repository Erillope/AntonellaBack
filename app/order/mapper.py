from ..common.table_mapper import TableMapper
from core.order.domain.order import Order, OrderFactory
from core.order.domain.item import ServiceItem, ServiceItemFactory, Payment
from core.order.domain.values import OrderStatusInfo, OrderStatus, PaymentStatus, PaymentType, Progresstatus, DateInfo
from .models import OrderTable, ServiceItemTable, PaymentTable

class OrderTableMapper(TableMapper[Order, OrderTable]):
    def to_table(self, model: Order) -> OrderTable:
        return OrderTable(
            id=model.id,
            client_id=model.client_id,
            status=model.status.status.lower(),
            progress_status=model.status.progress_status.lower(),
            payment_status=model.status.payment_status.lower(),
            payment_type=model.status.payment_type.lower(),
            created_date=model.created_date,
            card_charge=model.card_charge,
        )

    def from_table(self, table: OrderTable) -> Order:
        return OrderFactory.load(
            id=table.id,
            client_id=table.client_id,
            status=OrderStatusInfo(
                status=OrderStatus(table.status.capitalize()),
                progress_status=Progresstatus(table.progress_status.capitalize()),
                payment_status=PaymentStatus(table.payment_status.capitalize()),
                payment_type=PaymentType(table.payment_type.capitalize())
            ),
            card_charge=table.card_charge,
            created_date=table.created_date
        )


class ServiceItemTableMapper(TableMapper[ServiceItem, OrderTable]):
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
            base_price=model.price.base_price
        )
    
    def from_table(self, table: ServiceItemTable) -> ServiceItem:
        return ServiceItemFactory.load(
            id=table.id,
            service_id=table.service_id,
            order_id=table.order_id,
            day= DateInfo(
                day=table.date_info_day,
                start_time=table.date_info_start_time,
                end_time=table.date_info_end_time
            ),
            status=Progresstatus(table.status.capitalize()),
            price=table.base_price,
            payment_percentage=table.payment_percentage,
            payments=[
                Payment(
                    employee_id=payment.employee_id,
                    percentage=payment.percentage,
                    amount=payment.amount
                ) for payment in PaymentTable.from_service_item(table.id)
            ],
            created_date=table.created_date
        )