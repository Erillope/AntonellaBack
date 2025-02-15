from __future__ import annotations
from core.common import Event
from core.common.image_storage import Base64ImageStorage
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .store_service import StoreService
    from .question import Question
    

class StoreServiceSaved(Event):
    '''Evento para cuando un servicio de tienda es actualizado'''
    def __init__(self, store_service: StoreService):
        self.store_service = store_service


class StoreServiceDeleted(Event):
    '''Evento para cuando un servicio de tienda es eliminado'''
    def __init__(self, store_service_id: str):
        self.store_service_id = store_service_id


class StoreServiceImageAdded(Event):
    '''Evento para cuando una imagen es agregada a un servicio de tienda'''
    def __init__(self, store_service_id: str, image: Base64ImageStorage):
        self.store_service_id = store_service_id
        self.image = image


class StoreServiceImageDeleted(Event):
    '''Evento para cuando una imagen es eliminada de un servicio de tienda'''
    def __init__(self, store_service_id: str, image_url: str):
        self.store_service_id = store_service_id
        self.image_url = image_url


class QuestionCreated(Event):
    '''Evento para cuando una pregunta de formulario es creada'''
    def __init__(self, question: Question):
        self.question = question


class QuestionDeleted(Event):
    '''Evento para cuando una pregunta de formulario es eliminada'''
    def __init__(self, question_id: str):
        self.question_id = question_id


class ChoiceAdded(Event):
    '''Evento para cuando una imagen es agregada a una opción de pregunta de selección'''
    def __init__(self, question_id: str, option: str, image: Optional[Base64ImageStorage]=None):
        self.question_id = question_id
        self.option = option
        self.image = image


class ChoiceDeleted(Event):
    '''Evento para cuando una imagen es eliminada de una opción de pregunta de selección'''
    def __init__(self, question_id: str, option: str):
        self.question_id = question_id
        self.option = option