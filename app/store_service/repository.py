from app.common.django_repository import DjangoSaveModel, DjangoDeleteModel, DjangoGetModel
from core.store_service import StoreService, Question, ImageChoiceQuestion, TextChoiceQuestion
from .models import StoreServiceTableData, StoreServiceImage, QuestionTableData, QuestionChoice, ChoiceImage, StoreServicePrice
from core.common import EventSubscriber, Event
from app.common.exceptions import ModelNotFoundException
from core.store_service.domain.events import (StoreServiceSaved, StoreServiceDeleted, QuestionSaved,
                                              QuestionDeleted)
from .mapper import StoreServiceTableMapper, QuestionTableMapper
from typing import List, Optional
from core.store_service.service.repository import GetQuestion, GetService
from core.common import ID
from django.db.models import Q

class DjangoGetStoreService(DjangoGetModel[StoreServiceTableData, StoreService], GetService):
    def __init__(self) -> None:
        super().__init__(StoreServiceTableData, StoreServiceTableMapper())
        self._filter = Q()
    
    def find_by_name(self, name: str) -> List[StoreService]:
        services = StoreServiceTableData.objects.filter(name__icontains=name.lower())
        return [self.mapper.to_model(service) for service in services]
    
    def find_by_type(self, type: str) -> List[StoreService]:
        services = StoreServiceTableData.objects.filter(type=type.upper())
        return [self.mapper.to_model(service) for service in services]
    
    def prepare_service_name_filter(self, name: str) -> None:
        self._filter &= Q(name__icontains=name.lower())
    
    def prepare_service_type_filter(self, type: str) -> None:
        self._filter &= Q(type=type.upper())
    
    def get_filtered_services(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[StoreService]:
        services = StoreServiceTableData.objects.filter(self._filter).distinct()
        if limit and offset:
            services = services[offset:offset + limit]
        if limit:
            services = services[:limit]
        if offset:
            services = services[offset:]
        self._filter = Q()
        return [self.mapper.to_model(service) for service in services]
    
    
class DjangoSaveStoreService(DjangoSaveModel[StoreServiceTableData, StoreService], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(StoreServiceTableMapper())
        EventSubscriber.__init__(self)
    
    def save(self, store_service: StoreService) -> None:
        super().save(store_service)
        self.save_images(store_service)
        self.save_prices(store_service)
        
    def save_images(self, store_service: StoreService) -> None:
        StoreServiceImage.objects.filter(service__id=store_service.id).delete()
        for image in store_service.images:
            StoreServiceImage.objects.create(image=image, service_id=store_service.id)
    
    def save_prices(self, store_service: StoreService) -> None:
        StoreServicePrice.objects.filter(service__id=store_service.id).delete()
        for price in store_service.prices:
            StoreServicePrice.objects.create(name=price.name,
                                             min_price=price.range.min,
                                             max_price=price.range.max,
                                             service_id=store_service.id)
            
    def handle(self, event: Event) -> None:
        if isinstance(event, StoreServiceSaved):
            self.save(event.store_service)
        


class DjangoDeleteStoreService(DjangoDeleteModel[StoreServiceTableData, StoreService], EventSubscriber):
    def __init__(self) -> None:
        get_store_service = DjangoGetModel[StoreServiceTableData, StoreService](StoreServiceTableData, StoreServiceTableMapper())
        super().__init__(StoreServiceTableData, StoreServiceTableMapper(), get_store_service)
        EventSubscriber.__init__(self)
    
    def handle(self, event: Event) -> None:
        if isinstance(event, StoreServiceDeleted):
            self.delete(event.store_service.id)


class DjangoSaveQuestion(DjangoSaveModel[QuestionTableData, Question], EventSubscriber):
    def __init__(self) -> None:
        super().__init__(QuestionTableMapper())
        EventSubscriber.__init__(self)
    
    def save(self, question: Question) -> None:
        super().save(question)
        self.save_choices(question)
    
    def save_choices(self, question: Question) -> None:
        QuestionChoice.objects.filter(question__id=question.id).delete()
        if isinstance(question, TextChoiceQuestion):
            for option in question.choices:
                QuestionChoice.objects.create(option=option, question_id=question.id)
        elif isinstance(question, ImageChoiceQuestion):
            for choice in question.choices:
                choice_table = QuestionChoice.objects.create(option=choice.option, question_id=question.id)
                ChoiceImage.objects.create(image=choice.image, choice=choice_table)
        
    def handle(self, event: Event) -> None:
        if isinstance(event, QuestionSaved):
            self.save(event.question)


class DjangoGetQuestion(DjangoGetModel[QuestionTableData, Question], GetQuestion):
    def __init__(self) -> None:
        super().__init__(QuestionTableData, QuestionTableMapper())
    
    def exists(self, unique: str) -> bool:
        if ID.is_id(unique): return super().exists(unique)
        return self.exists_by_title(unique)
    
    def exists_by_title(self, title: str) -> bool:
        return QuestionTableData.objects.filter(title=title.lower()).exists()
    
    def get(self, unique: str) -> Question:
        if ID.is_id(unique): return super().get(unique)
        return self.get_by_title(unique)
    
    def get_by_title(self, title: str) -> Question:
        if not self.exists_by_title(title): raise ModelNotFoundException.not_found(title)
        question_table = QuestionTableData.objects.get(title=title.lower())
        return self.mapper.to_model(question_table)
    
    def get_service_questions(self, service_id: str) -> List[Question]:
        question_tables = QuestionTableData.service_questions(service_id)
        return [self.mapper.to_model(question_table) for question_table in question_tables]
    
    
class DjangoDeleteQuestion(DjangoDeleteModel[QuestionTableData, Question], EventSubscriber):
    def __init__(self) -> None:
        get_question = DjangoGetQuestion()
        super().__init__(QuestionTableData, QuestionTableMapper(), get_question)
        EventSubscriber.__init__(self)
        
    def handle(self, event: Event) -> None:
        if isinstance(event, QuestionDeleted):
            self.delete(event.question.id)