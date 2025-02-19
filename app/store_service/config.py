from app.common.django_repository import DjangoGetModel
from .repository import (DjangoSaveStoreService, DjangoDeleteStoreService, DjangoSaveQuestion, 
                         DjangoDeleteQuestion, DjangoGetQuestion)
from .mapper import StoreServiceTableMapper
from .models import StoreServiceTableData
from core.store_service import StoreService, StoreServices, QuestionService

get_store_service = DjangoGetModel[StoreServiceTableData, StoreService](
    mapper=StoreServiceTableMapper(),
    table=StoreServiceTableData
)

save_store_service = DjangoSaveStoreService()

delete_store_service = DjangoDeleteStoreService()

get_question = DjangoGetQuestion()

save_question = DjangoSaveQuestion()

delete_question = DjangoDeleteQuestion()

question_service = QuestionService(
    get_question=get_question,
)

store_services = StoreServices(
    get_service=get_store_service,
    question_service=question_service
)