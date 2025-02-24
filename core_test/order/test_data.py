import json
from core.order import ServiceItem, ServiceItemFactory
from core.common import ID
import random
from decimal import Decimal
from datetime import date, time
from core.order.domain.values import Price
from core.common.config import AppConfig

class DataFactory:
    
    @classmethod
    def generate_service_items(cls) -> ServiceItem:
        return ServiceItemFactory.create(
            service_id=ID.generate(),
            order_id=ID.generate(),
            payment_percentage=Decimal(random.random()),
            day=date(random.randint(2020, 2021), random.randint(1, 12), random.randint(1, 28)),
            start_time=time(random.randint(8, 18), random.randint(0, 59)),
            end_time=time(random.randint(9, 19), random.randint(0, 59)),
            price= Price(base_price= Decimal(random.randint(20, 500)), sale_price= Decimal(random.randint(30, 500)),
                        iva= AppConfig.iva(), card_charge= Decimal(random.randint(30, 100)))
        )
    
    @classmethod
    def create_service_items_invalid_percentage(cls) -> ServiceItem:
            ServiceItemFactory.create(
                service_id=ID.generate(),
                order_id=ID.generate(),
                payment_percentage=cls._generate_invalid_percentage(),
                day=date.today(),
                start_time=time(random.randint(8, 18), random.randint(0, 59)),
                end_time=time(random.randint(9, 19), random.randint(0, 59)),
                price=Price(base_price= Decimal(random.randint(20, 500)), sale_price= Decimal(random.randint(30, 500)),
                        iva= AppConfig.iva(), card_charge= Decimal(random.randint(30, 100)))
            )

    @classmethod
    def create_service_items_invalid_time(cls) -> ServiceItem:
            ServiceItemFactory.create(
                service_id=ID.generate(),
                order_id=ID.generate(),
                payment_percentage=Decimal(random.random()),
                day=date.today(),
                start_time=time(random.randint(0, 7), random.randint(0, 59)),
                end_time=time(random.randint(20, 23), random.randint(0, 59)),
                price=Price(base_price= Decimal(random.randint(20, 500)), sale_price= Decimal(random.randint(30, 500)),
                        iva= AppConfig.iva(), card_charge= Decimal(random.randint(30, 100)))
            )
    
    def _generate_invalid_percentage() -> Decimal:
        if random.choice([True, False]):
            return Decimal(random.uniform(-1, -0.01))
        else:
            return Decimal(random.uniform(1.01, 2))


