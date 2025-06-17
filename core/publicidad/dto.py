from pydantic import BaseModel
from typing import List, Optional
from .publicidad import ItemData
from datetime import date

class CreatePublicidadDTO(BaseModel):
    title: str
    description: str
    images: List[str]
    service_items: List[ItemData]
    product_items: List[ItemData]


class UpdatePublicidadDTO(BaseModel):
    id: str
    title: Optional[str] = None
    images: Optional[List[str]] = None
    service_items: Optional[List[ItemData]] = None
    product_items: Optional[List[ItemData]] = None


class PublicidadDTO(BaseModel):
    id: str
    title: str
    description: str
    images: List[str]
    service_items: List[ItemData]
    product_items: List[ItemData]
    created_date: date