from __future__ import annotations
from core.common import Event
from core.common.image_storage import Base64ImageStorage, ImageSaved, ImageDeleted
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .store_service import StoreService
    from .question import Question    

class StoreServiceSaved(Event):
    '''Evento para cuando un servicio de tienda es actualizado'''
    def __init__(self, store_service: StoreService):
        self.store_service = store_service


class StoreServiceDeleted(ImageDeleted):
    '''Evento para cuando un servicio de tienda es eliminado'''
    def __init__(self, store_service: StoreService):
        super().__init__(store_service.images)
        self.store_service = store_service


class StoreServiceImageAdded(ImageSaved):
    '''Evento para cuando una imagen es agregada a un servicio de tienda'''
    def __init__(self, store_service_id: str, image: Base64ImageStorage):
        super().__init__([image])
        self.image = image
        self.store_service_id = store_service_id


class StoreServiceImageDeleted(ImageDeleted):
    '''Evento para cuando una imagen es eliminada de un servicio de tienda'''
    def __init__(self, store_service_id: str, image_url: str):
        super().__init__([image_url])
        self.image_url = image_url
        self.store_service_id = store_service_id


class QuestionSaved(Event):
    '''Evento para cuando una pregunta de formulario es creada'''
    def __init__(self, question: Question):
        self.question = question


class QuestionDeleted(ImageDeleted):
    '''Evento para cuando una pregunta de formulario es eliminada'''
    def __init__(self, question: Question):
        from .question import ImageChoiceQuestion
        if isinstance(question, ImageChoiceQuestion):
            super().__init__([choice.image_url for choice in question.choices])
        else:
            super().__init__([])
        self.question = question


class ChoiceAdded(Event):
    '''Evento para cuando una imagen es agregada a una opción de pregunta de selección'''
    def __init__(self, question_id: str, option: str):
        self.question_id = question_id
        self.option = option

class ChoiceImageAdded(ImageSaved):
    '''Evento para cuando una imagen es agregada a una opción de pregunta de selección'''
    def __init__(self, question_id: str, option: str, image: Base64ImageStorage):
        super().__init__([image])
        self.image = image
        self.question_id = question_id
        self.option = option


class ChoiceDeleted(Event):
    '''Evento para cuando una imagen es eliminada de una opción de pregunta de selección'''
    def __init__(self, question_id: str, option: str):
        self.question_id = question_id
        self.option = option


class ChoiceImageDeleted(ImageDeleted):
    '''Evento para cuando una imagen es eliminada de una opción de pregunta de selección'''
    def __init__(self, question_id: str, option: str, image_url: str):
        super().__init__([image_url])
        self.question_id = question_id
        self.option = option