from pydantic import BaseModel
from core.store_service.domain.values import ServiceType
from core.product.domain.values import ProductStatus
from decimal import Decimal
from typing import Optional, List
from datetime import date

class CreateProductDto(BaseModel):
    name: str
    service_type: ServiceType
    service_subtype: str
    product_type: str
    volume: int
    description: str
    price: Decimal
    stock: int
    images: list[str]


class UpdateProductDto(BaseModel):
    id: str
    name: Optional[str] = None
    service_type: Optional[ServiceType] = None
    service_subtype: Optional[str] = None
    product_type: Optional[str] = None
    volume: Optional[int] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    additional_stock: int = 0
    images: Optional[list[str]] = None
    status: Optional[ProductStatus] = None


class ProductDto(BaseModel):
    id: str
    name: str
    service_type: ServiceType
    service_subtype: str
    product_type: str
    volume: int
    description: str
    price: Decimal
    stock: int
    images: List[str]
    status: ProductStatus
    stock_modified_date: date
    created_date: date


class ProductFilterDto(BaseModel):
    name: Optional[str] = None
    service_type: Optional[ServiceType] = None
    start_stock_modified_date: Optional[date] = None
    end_stock_modified_date: Optional[date] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    only_count: bool = False


class ProductFilterResponseDto(BaseModel):
    products: List[ProductDto]
    total_count: int
    filtered_count: int