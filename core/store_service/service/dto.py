from pydantic import BaseModel
from core.store_service import ServiceType, ServiceStatus
from core.common import OrdenDirection
from typing import List, Optional
from datetime import date

class CreateStoreServiceDto(BaseModel):
    name: str
    description: str
    type: ServiceType
    images: List[str] = []


class UpdateStoreServiceDto(BaseModel):
    id: str
    name: Optional[str]=None
    description: Optional[str]=None
    type: Optional[ServiceType]=None
    status: Optional[ServiceStatus]=None


class FilterStoreServiceDto(BaseModel):
    expresion: Optional[str] = None
    order_by: str
    offset: Optional[int] = None
    limit: Optional[int] = None
    order_direction: OrdenDirection = OrdenDirection.DESC


class StoreServiceDto(BaseModel):
    id: str
    name: str
    description: str
    status: ServiceStatus
    type: ServiceType
    images: List[str] = []
    created_date: date