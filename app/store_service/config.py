from .repository import (DjangoSaveStoreService, DjangoDeleteStoreService, DjangoSaveQuestion, 
                         DjangoDeleteQuestion, DjangoGetQuestion, DjangoGetStoreService)
from core.store_service import StoreServices, QuestionService

get_store_service = DjangoGetStoreService()

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