from core.common.abstract_repository import GetModel
from .publicidad import Publicidad
from abc import ABC, abstractmethod
from typing import List, Tuple
from .dto import FilterPublicidadDTO

class GetPublicidad(GetModel[Publicidad], ABC):
    @abstractmethod
    def get_related_publicidad(self, services_id: List[str], products_id: List[str]) -> List[Publicidad]: ...

    @abstractmethod
    def filter_publicidad(self, filter_dto: FilterPublicidadDTO) -> Tuple[List[Publicidad], int]: ...
