from app.common.django_repository import DjangoGetModel
from .repository import DjangoSaveStoreService, DjangoDeleteStoreService
from .mapper import StoreServiceTableMapper
from .models import StoreServiceTableData
from core.store_service import StoreService, StoreServices

get_store_service = DjangoGetModel[StoreServiceTableData, StoreService](
    mapper=StoreServiceTableMapper(),
    table=StoreServiceTableData
)

save_store_service = DjangoSaveStoreService()

delete_store_service = DjangoDeleteStoreService()

store_services = StoreServices(
    get_service=get_store_service
)