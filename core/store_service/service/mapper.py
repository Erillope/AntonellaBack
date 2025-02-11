from core.store_service import StoreService, StoreServiceFactory
from .dto import CreateStoreServiceDto, StoreServiceDto

class StoreServiceMapper:
    @staticmethod
    def to_store_service(dto: CreateStoreServiceDto) -> StoreService:
        return StoreServiceFactory.create(
            name=dto.name,
            description=dto.description,
            type=dto.type,
            images=dto.images
        )
    
    @staticmethod
    def to_dto(domain: StoreService) -> StoreServiceDto:
        return StoreServiceDto(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            status=domain.status,
            type=domain.type,
            images=domain.images,
            created_date=domain.created_date
        )