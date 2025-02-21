import json
from decimal import Decimal
from datetime import time

MEDIA = 'resources/media'

class AppConfig:
    data = {}
    with open('resources/config.json') as file:
        data = json.load(file)
    
    @classmethod
    def payment_percentage(cls) -> Decimal:
        return Decimal(cls.data.get('payment_percentage', 0.5))

    @classmethod
    def start_time(cls) -> time:
        return time.fromisoformat(cls.data.get('start_time', '08:00:00'))
    
    @classmethod
    def end_time(cls) -> time:
        return time.fromisoformat(cls.data.get('end_time', '20:00:00'))
    
    @classmethod
    def iva(cls) -> Decimal:
        return Decimal(cls.data.get('IVA', 0.15))