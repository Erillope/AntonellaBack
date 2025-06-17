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
            description=publicidad.description
        )
    
    @classmethod
    def to_publicidad(cls, dto: CreatePublicidadDTO) -> Publicidad:
        return PublicidadFactory.create(
            title=dto.title,
            images=dto.images,
            desciption=dto.description,
            service_items=dto.service_items,
            product_items=dto.product_items
        )