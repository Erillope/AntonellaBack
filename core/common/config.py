import json
from decimal import Decimal
from datetime import time
from typing import Dict, Any, List
import os

DIR = os.path.sep.join(os.path.join(os.path.dirname(__file__)).split(os.path.sep)[0:-2])
resources_path = os.path.join(DIR, 'resources')

MEDIA = "resources_test/media/"

class AppConfig:
    server_host = "https://erillope.pythonanywhere.com/"
    client_host = "http://localhost:5173/"
    reset_password_url = client_host + "password/reset/"
    data = {}
    with open(os.path.join(resources_path, "config.json"), encoding='utf-8') as file:
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
        return Decimal(cls.data.get('iva', 15.00))
    
    @classmethod
    def default_super_admin(cls) -> Dict[str, Any]:
        super_admin_data =  cls.data.get('default_super_admin', {})
        super_admin_data['photo'] = os.path.join(MEDIA, super_admin_data['photo'])
        return super_admin_data 

    @classmethod
    def reset_password_message(cls, user_name: str, token_id: str) -> str:
        message: str = cls.data.get('reset_password_message', 'Null message')
        return message % (user_name, f"{cls.reset_password_url}{token_id}")
    
    @classmethod
    def email_password(cls) -> str:
        return cls.data.get('email_password', '')
    
    @classmethod
    def app_email(cls) -> str:
        return cls.data.get('app_email', '')
    
    @classmethod
    def categories_subtypes(cls) -> Dict[str, Any]:
        return cls.data.get('categories_subtypes', {})
    
    @classmethod
    def producy_types(cls) -> List[str]:
        return cls.data.get('product_types', [])