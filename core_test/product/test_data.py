from core.product import Product, ProductFactory
from core.product.domain.values import ProductStatus, ProductName
from core.store_service import ServiceType
import lorem  #type: ignore
import random
from core_test.images_data import get_base64_string
from decimal import Decimal
from typing import Dict, Any
from core.common.config import AppConfig

class ProductTestData:
    @classmethod
    def generate_product(cls) -> Product:
        return ProductFactory.create(**cls.product_data())
    
    @classmethod
    def product_data(cls) -> Dict[str, Any]:
        return {
            'name': ProductName.MATCHER.generate(),
            'service_type': random.choice(list(ServiceType)),
            'description': lorem.sentence(),
            'price': Decimal(random.randint(1, 100)),
            'stock': random.randint(1, 100),
            'images': [
                get_base64_string() for _ in range(3)
            ],
            'service_subtype': random.choice(list(ServiceType)),
            'product_type': random.choice(AppConfig.producy_types()),
            'volume': random.randint(1, 100),
        }
    
    @classmethod
    def product_update_data(cls) -> Dict[str, Any]:
        return {
            'name': ProductName.MATCHER.generate(),
            'service_type': random.choice(list(ServiceType)),
            'description': lorem.sentence(),
            'price': Decimal(random.randint(1, 100)),
            'additional_stock': random.randint(1, 100),
            'images': [
                get_base64_string() for _ in range(3)
            ],
            'status': random.choice(list(ProductStatus)),
            'service_subtype': random.choice(list(ServiceType)),
            'product_type': random.choice(AppConfig.producy_types()),
            'volume': random.randint(1, 100),
        }