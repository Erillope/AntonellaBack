from pydantic import BaseModel
from core.store_service.domain.values import ServiceType
from decimal import Decimal
from typing import Optional

class CreateProductDto(BaseModel):
    name: str
    service_type: ServiceType
    description: str
    price: Decimal
    stock: int
    images: list[str]


class UpdateProductDto(BaseModel):
    id: str
    name: Optional[str] = None
    service_type: Optional[ServiceType] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    additional_stock: int = 0
    images: Optional[list[str]] = None


class ProductDto(BaseModel):
    id: str
    name: str
    service_type: ServiceType
    description: str
    price: Decimal
    stock: int
    images: list[str]