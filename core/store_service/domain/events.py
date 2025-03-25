from __future__ import annotations
from core.common import Event
from core.common.image_storage import ImageDeleted
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
        

class QuestionSaved(Event):
    '''Evento para cuando una pregunta de formulario es creada'''
    def __init__(self, question: Question):
        self.question = question


class QuestionDeleted(ImageDeleted):
    '''Evento para cuando una pregunta de formulario es eliminada'''
    def __init__(self, question: Question):
        from .question import ImageChoiceQuestion
        if isinstance(question, ImageChoiceQuestion):
            super().__init__([choice.image for choice in question.choices])
        else:
            super().__init__([])
        self.question = question