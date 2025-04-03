from core_test.product.test_data import ProductTestData as CoreProductTestData
from typing import Dict, Any
from core_test.images_data import get_base64_string
import random

class ProductTestData(CoreProductTestData):
    @classmethod
    def generate_create_product_request(cls) -> Dict[str, Any]:
        product = cls.generate_product()
        return {
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'images': [get_base64_string() for _ in range(3)],
            'stock': product.stock,
            'service_type': product.service_type.value,
            'service_subtype': product.service_subtype,
            'product_type': product.product_type,
            'volume': product.volume,
        }
    
    @classmethod
    def generate_update_product_request(cls, id: str) -> Dict[str, Any]:
        product = cls.generate_product()
        return {
            'id': id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'images': [get_base64_string() for _ in range(3)],
            'additional_stock': random.randint(1, 10),
            'service_type': product.service_type.value,
            'status': product.status.value,
            'service_subtype': product.service_subtype,
            'product_type': product.product_type,
            'volume': product.volume,
        }