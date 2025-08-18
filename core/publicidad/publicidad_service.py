from abc import ABC, abstractmethod
from typing import List
from .repository import GetPublicidad
from .dto import CreatePublicidadDTO, FilterPublicidadDTO, UpdatePublicidadDTO, PublicidadDTO, FilterPublicidadResponse
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

    @abstractmethod
    def get_related_publicidad(self, services_id: List[str], products_id: List[str]) -> List[PublicidadDTO]: ...

    @abstractmethod
    def filter_publicidad(self, filter_dto: FilterPublicidadDTO) -> FilterPublicidadResponse: ...


class PublicidadService(AbstractPublicidadService):
    def __init__(self, get_publicidad: GetPublicidad) -> None:
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
            description=dto.description,
            service_items=dto.service_items,
            product_items=dto.product_items,
            enabled=dto.enabled
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
    
    def get_related_publicidad(self, services_id: List[str], products_id: List[str]) -> List[PublicidadDTO]:
        publicidades = self._get_publicidad.get_related_publicidad(services_id, products_id)
        return [PublicidadMapper.to_dto(pub) for pub in publicidades]

    def filter_publicidad(self, filter_dto: FilterPublicidadDTO) -> FilterPublicidadResponse:
        publicidades, filtered_count = self._get_publicidad.filter_publicidad(filter_dto)
        total_count = self._get_publicidad.total_count()
        return FilterPublicidadResponse(
            total_count=total_count,
            filtered_count=filtered_count,
            publicidades=[PublicidadMapper.to_dto(pub) for pub in publicidades]
        )