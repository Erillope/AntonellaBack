from __future__ import annotations
from core.common import Event
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .store_service import StoreService
    

class StoreServiceSaved(Event):
    '''Evento para cuando un servicio de tienda es actualizado'''
    def __init__(self, store_service: StoreService):
        self.store_service = store_service


class StoreServiceDeleted(Event):
    '''Evento para cuando un servicio de tienda es eliminado'''
    def __init__(self, store_service_id: str):
        self.store_service_id = store_service_id