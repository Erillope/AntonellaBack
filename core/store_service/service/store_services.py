from .abstract_services import AbstractStoreServices, AbstractQuestionService
from .dto import (StoreServiceDto, CreateStoreServiceDto, UpdateStoreServiceDto, FilterStoreServiceDto,
                  CreateQuestionDto, QuestionDto, UpdateQuestionDto)
from typing import List, Optional
from .repository import GetQuestion, GetService
from core.common.abstract_repository import GetModel
from core.store_service import StoreService, ImageChoiceQuestion, TextChoiceQuestion, Choice
from .mapper import StoreServiceMapper, QuestionMapper

class QuestionService(AbstractQuestionService):
    def __init__(self, get_question: GetQuestion) -> None:
        self.get_question = get_question
        
    def create(self, service_id: str, dto: CreateQuestionDto) -> QuestionDto:
        question = QuestionMapper.to_question(dto)
        question.set_store_service(service_id)
        question.save()
        return QuestionMapper.to_dto(question)

    def update(self, dto: UpdateQuestionDto) -> QuestionDto:
        question = self.get_question.get(dto.id)
        question.change_data(dto.title)
        if isinstance(question, TextChoiceQuestion) and dto.choices:
            question.change_data(choices=[choice.option for choice in dto.choices])
        elif isinstance(question, ImageChoiceQuestion) and dto.choices:
            question.change_data(choices=[Choice(option=choice.option, image=choice.image) for choice in dto.choices])
        question.save()
        return QuestionMapper.to_dto(question)
    
    def delete(self, id: str) -> QuestionDto:
        question = self.get_question.get(id)
        question.delete()
        return QuestionMapper.to_dto(question)
    
    def find(self, id: str) -> QuestionDto:
        question = self.get_question.get(id)
        return QuestionMapper.to_dto(question)
    
    def service_questions(self, service_id: str) -> List[QuestionDto]:
        questions = self.get_question.get_service_questions(service_id)
        return [QuestionMapper.to_dto(question) for question in questions]


class StoreServices(AbstractStoreServices):
    def __init__(self, get_service: GetService,
                 question_service: AbstractQuestionService) -> None:
        self.get_service = get_service
        self.question_service = question_service
    
    def create(self, dto: CreateStoreServiceDto) -> StoreServiceDto:
        service = StoreServiceMapper.to_store_service(dto)
        service.save()
        questions = [self.question_service.create(service.id, question) for question in dto.questions]
        return StoreServiceMapper.to_dto(service, questions)
    
    def update(self, dto: UpdateStoreServiceDto) -> StoreServiceDto:
        service = self.get_service.get(dto.id)
        service.change_data(
            name=dto.name,
            description=dto.description,
            type=dto.type,
            status=dto.status,
            duration=dto.duration,
            images=dto.images,
            prices=dto.prices,
            subtype=dto.subtype
        )
        service.save()
        return self.find(service.id)
    
    def delete(self, id: str) -> StoreServiceDto:
        service = self.get_service.get(id)
        service_dto = self.find(id)
        service.delete()
        return service_dto
    
    def find(self, id: str) -> StoreServiceDto:
        service = self.get_service.get(id)
        questions = self.question_service.service_questions(service.id)
        return StoreServiceMapper.to_dto(service, questions)
    
    def find_by_name(self, name: str) -> List[StoreServiceDto]:
        service = self.get_service.find_by_name(name)
        dtos: List[StoreServiceDto] = []
        for s in service:
            questions = self.question_service.service_questions(s.id)
            dtos.append(StoreServiceMapper.to_dto(s, questions))
        return dtos
    
    def find_by_type(self, type: str) -> List[StoreServiceDto]:
        service = self.get_service.find_by_type(type)
        dtos: List[StoreServiceDto] = []
        for s in service:
            questions = self.question_service.service_questions(s.id)
            dtos.append(StoreServiceMapper.to_dto(s, questions))
        return dtos
    
    def filter(self, dto: FilterStoreServiceDto) -> List[StoreServiceDto]:
        services = self.get_service.filter(
            order_by=dto.order_by,
            offset=dto.offset,
            limit=dto.limit,
            direction=dto.order_direction
        )
        return [self.find(service.id) for service in services]
    
    def get_all(self) -> List[StoreServiceDto]:
        services = self.get_service.get_all()
        return [self.find(service.id) for service in services]