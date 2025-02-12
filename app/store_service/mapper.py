from app.common.table_mapper import TableMapper
from .models import StoreServiceTableData
from core.store_service import (StoreService, StoreServiceFactory,
                                                     ServiceStatus, ServiceType)

class StoreServiceTableMapper(TableMapper[StoreServiceTableData, StoreService]):
    def to_table(self, store_service: StoreService) -> StoreServiceTableData:
        return StoreServiceTableData(
            id=store_service.id,
            name=store_service.name,
            description=store_service.description,
            status=store_service.status.value,
            type=store_service.type.value,
            created_date=store_service.created_date
        )
    
    def to_model(self, store_service_table: StoreServiceTableData) -> StoreService:
        return StoreServiceFactory.load(
            id=str(store_service_table.id),
            name=store_service_table.name,
            description=store_service_table.description,
            status=ServiceStatus(store_service_table.status),
            type=ServiceType(store_service_table.type),
            created_date=store_service_table.created_date
        )