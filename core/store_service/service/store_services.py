from abc import ABC, abstractmethod
from .dto import StoreServiceDto, CreateStoreServiceDto, UpdateStoreServiceDto, FilterStoreServiceDto
from typing import List
from core.common.abstract_repository import GetModel
from core.store_service import StoreService
from .mapper import StoreServiceMapper

class AbstractStoreServices(ABC):
    @abstractmethod
    def create(self, dto: CreateStoreServiceDto) -> StoreServiceDto: ...
    
    @abstractmethod
    def update(self, dto: UpdateStoreServiceDto) -> StoreServiceDto: ...
    
    @abstractmethod
    def delete(self, id: str) -> StoreServiceDto: ...
    
    @abstractmethod
    def find(self, id: str) -> StoreServiceDto: ...
    
    @abstractmethod
    def filter(self, dto: FilterStoreServiceDto) -> List[StoreServiceDto]: ...
    
    @abstractmethod
    def add_image(self, service_id: str, image: str) -> StoreServiceDto: ...
    
    @abstractmethod
    def delete_image(self, service_id: str, image: str) -> StoreServiceDto: ...


class StoreServices(AbstractStoreServices):
    def __init__(self, get_service: GetModel[StoreService]) -> None:
        self.get_service = get_service
    
    def create(self, dto: CreateStoreServiceDto) -> StoreServiceDto:
        service = StoreServiceMapper.to_store_service(dto)
        for image in dto.images:
            service.add_image(image)
        service.save()
        return StoreServiceMapper.to_dto(service)
    
    def update(self, dto: UpdateStoreServiceDto) -> StoreServiceDto:
        service = self.get_service.get(dto.id)
        service.change_data(
            name=dto.name,
            description=dto.description,
            type=dto.type,
            status=dto.status
        )
        service.save()
        return StoreServiceMapper.to_dto(service)
    
    def delete(self, id: str) -> StoreServiceDto:
        service = self.get_service.get(id)
        service.delete()
        return StoreServiceMapper.to_dto(service)
    
    def find(self, id: str) -> StoreServiceDto:
        service = self.get_service.get(id)
        return StoreServiceMapper.to_dto(service)
    
    def filter(self, dto: FilterStoreServiceDto) -> List[StoreServiceDto]:
        services = self.get_service.filter(
            expresion=dto.expresion,
            order_by=dto.order_by,
            offset=dto.offset,
            limit=dto.limit,
            direction=dto.order_direction
        )
        return [StoreServiceMapper.to_dto(service) for service in services]
    
    def add_image(self, service_id: str, image: str) -> StoreServiceDto:
        service = self.get_service.get(service_id)
        service.add_image(image)
        service.save()
        return StoreServiceMapper.to_dto(service)
    
    def delete_image(self, service_id: str, image: str) -> StoreServiceDto:
        service = self.get_service.get(service_id)
        service.delete_image(image)
        service.save()
        return StoreServiceMapper.to_dto(service)