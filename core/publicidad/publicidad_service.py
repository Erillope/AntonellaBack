from abc import ABC, abstractmethod
from typing import List
from core.common.abstract_repository import GetModel
from .publicidad import Publicidad
from .dto import CreatePublicidadDTO, UpdatePublicidadDTO, PublicidadDTO
from .mapper import PublicidadMapper

class AbstractPublicidadService(ABC):
    @abstractmethod
    def create_publicidad(self, dto: CreatePublicidadDTO) -> PublicidadDTO:...

    @abstractmethod
    def update_publicidad(self, dto: UpdatePublicidadDTO) -> PublicidadDTO: ...

    @abstractmethod
    def delete_publicidad(self, id: str) -> None: ...

    @abstractmethod
    def get_publicidad(self, id: str) -> PublicidadDTO: ...

    @abstractmethod
    def get_all(self) -> List[PublicidadDTO]: ...


class PublicidadService(AbstractPublicidadService):
    def __init__(self, get_publicidad: GetModel[Publicidad]):
        self._get_publicidad = get_publicidad
    
    def create_publicidad(self, dto: CreatePublicidadDTO) -> PublicidadDTO:
        publicidad = PublicidadMapper.to_publicidad(dto)
        publicidad.save()
        return PublicidadMapper.to_dto(publicidad)
    
    def update_publicidad(self, dto: UpdatePublicidadDTO) -> PublicidadDTO:
        publicidad = self._get_publicidad.get(dto.id)
        publicidad.change_data(
            title=dto.title,
            images=dto.images,
            service_items=dto.service_items,
            product_items=dto.product_items
        )
        publicidad.save()
        return PublicidadMapper.to_dto(publicidad)
    
    def delete_publicidad(self, id: str) -> None:
        publicidad = self._get_publicidad.get(id)
        publicidad.delete()
    
    def get_all(self) -> List[PublicidadDTO]:
        publicidades = self._get_publicidad.get_all()
        return [PublicidadMapper.to_dto(pub) for pub in publicidades]
    
    def get_publicidad(self, id: str) -> PublicidadDTO:
        publicidad = self._get_publicidad.get(id)
        return PublicidadMapper.to_dto(publicidad)