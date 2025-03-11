import json
from decimal import Decimal
from datetime import time
from typing import Dict, Any

MEDIA = 'resources/media'

class AppConfig:
    server_host = "http://127.0.0.1:8000/"
    client_host = "http://localhost:5173/"
    reset_password_url = client_host + "password/reset/"
    data = {}
    with open('resources/config.json', encoding='utf-8') as file:
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
    
    @classmethod
    def default_super_admin(cls) -> Dict[str, Any]:
        return cls.data.get('default_super_admin', {})

    @classmethod
    def reset_password_message(cls, user_name: str, token_id: str) -> str:
        message: str = cls.data.get('reset_password_message', 'Null message')
        return message % (user_name, f"{cls.reset_password_url}{token_id}")
    
    @classmethod
    def email_password(cls) -> str:
        return cls.data.get('email_password', '')