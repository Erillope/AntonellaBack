from __future__ import annotations
from core.common import Event
from core.common.image_storage import ImageDeleted
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .publicidad import Publicidad

class PublicidadSaved(Event):
    '''Evento para cuando una publicidad es actualizada'''
    def __init__(self, publicidad: Publicidad):
        self.publicidad = publicidad


class PublicidadDeleted(ImageDeleted):
    '''Evento para cuando una publicidad es eliminada'''
    def __init__(self, publicidad: Publicidad):
        super().__init__(publicidad.images)
        self.publicidad = publicidad