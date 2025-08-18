from pydantic import BaseModel
from typing import List, Optional
from .publicidad import ItemData
from datetime import date

class CreatePublicidadDTO(BaseModel):
    title: str
    description: str
    images: List[str]
    service_items: Optional[List[ItemData]] = None
    product_items: Optional[List[ItemData]] = None


class UpdatePublicidadDTO(BaseModel):
    id: str
    title: Optional[str] = None
    images: Optional[List[str]] = None
    description: Optional[str] = None
    service_items: Optional[List[ItemData]] = None
    product_items: Optional[List[ItemData]] = None
    enabled: Optional[bool] = None


class PublicidadDTO(BaseModel):
    id: str
    title: str
    description: str
    images: List[str]
    service_items: Optional[List[ItemData]] = None
    product_items: Optional[List[ItemData]] = None
    created_date: date
    enabled: bool = True


class FilterPublicidadDTO(BaseModel):
    title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    onlyCount: Optional[bool] = None


class FilterPublicidadResponse(BaseModel):
    total_count: int
    filtered_count: int
    publicidades: List[PublicidadDTO]