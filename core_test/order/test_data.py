from core.order import ServiceItem, ServiceItemFactory
from core.common import ID
import random
from decimal import Decimal
from datetime import date, time

class DataFactory:
    @classmethod
    def generate_service_items(cls) -> ServiceItem:
        return ServiceItemFactory.create(
            service_id=ID.generate(),
            order_id=ID.generate(),
            payment_percentage=Decimal(random.random()),
            day=date(random.randint(2020, 2021), random.randint(1, 12), random.randint(1, 28)),
            start_time=time(random.randint(0, 23), random.randint(0, 59)),
            end_time=time(random.randint(0, 23), random.randint(0, 59))
        )