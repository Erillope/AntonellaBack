from .dto import PublicidadDTO, CreatePublicidadDTO
from .publicidad import Publicidad, PublicidadFactory

class PublicidadMapper:
    @classmethod
    def to_dto(cls, publicidad: Publicidad) -> PublicidadDTO:
        return PublicidadDTO(
            id=publicidad.id,
            title=publicidad.title,
            images=publicidad.images,
            service_items=publicidad.service_items,
            product_items=publicidad.product_items,
            created_date=publicidad.created_date,
            description=publicidad.description,
            enabled=publicidad.enabled
        )
    
    @classmethod
    def to_publicidad(cls, dto: CreatePublicidadDTO) -> Publicidad:
        return PublicidadFactory.create(
            title=dto.title,
            images=dto.images,
            description=dto.description,
            service_items=dto.service_items if dto.service_items else [],
            product_items=dto.product_items if dto.product_items else []
        )