from .abstract_services import AbstractStoreServices, AbstractQuestionService
from .dto import (StoreServiceDto, CreateStoreServiceDto, UpdateStoreServiceDto, FilterStoreServiceDto,
                  CreateQuestionDto, QuestionDto)
from typing import List, Optional
from .repository import GetQuestion
from core.common.abstract_repository import GetModel
from core.store_service import StoreService, TextChoiceQuestion, ImageChoiceQuestion
from .exceptions import MissingImageException, QuestionAlreadyExistsException
from .mapper import StoreServiceMapper, QuestionMapper

class QuestionService(AbstractQuestionService):
    def __init__(self, get_question: GetQuestion) -> None:
        self.get_question = get_question
        
    def create(self, service_id: str, dto: CreateQuestionDto) -> QuestionDto:
        self._verify_already_exists_question(dto.title)
        question = QuestionMapper.to_question(dto)
        question.set_store_service(service_id)
        question.save()
        return QuestionMapper.to_dto(question)

    def update(self, id: str, title: Optional[str]=None) -> QuestionDto:
        if title: self._verify_already_exists_question(title)
        question = self.get_question.get(id)
        question.change_data(title)
        question.save()
        return QuestionMapper.to_dto(question)
    
    def delete(self, id: str) -> QuestionDto:
        question = self.get_question.get(id)
        question.delete()
        return QuestionMapper.to_dto(question)
    
    def find(self, id: str) -> QuestionDto:
        question = self.get_question.get(id)
        return QuestionMapper.to_dto(question)
    
    def add_choice(self, question_id: str, option: str, base64_image: Optional[str]=None) -> QuestionDto:
        question = self.get_question.get(question_id)
        if isinstance(question, TextChoiceQuestion):
            question.add_choice(option)
        if isinstance(question, ImageChoiceQuestion):
            if not base64_image: raise MissingImageException.missing_image()
            question.add_choice(option, base64_image)
        return QuestionMapper.to_dto(question)
    
    def delete_choice(self, question_id: str, option: str) -> QuestionDto:
        question = self.get_question.get(question_id)
        if isinstance(question, TextChoiceQuestion) or isinstance(question, ImageChoiceQuestion):
            question.remove_choice(option)
        return QuestionMapper.to_dto(question)
    
    def service_questions(self, service_id: str) -> List[QuestionDto]:
        questions = self.get_question.get_service_questions(service_id)
        return [QuestionMapper.to_dto(question) for question in questions]

    def _verify_already_exists_question(self, title: str) -> None:
        if self.get_question.exists(title):
            raise QuestionAlreadyExistsException.already_exists(title)


class StoreServices(AbstractStoreServices):
    def __init__(self, get_service: GetModel[StoreService],
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
            status=dto.status
        )
        service.save()
        return StoreServiceMapper.to_dto(service)
    
    def delete(self, id: str) -> StoreServiceDto:
        service = self.get_service.get(id)
        service_dto = self.find(id)
        service.delete()
        return service_dto
    
    def find(self, id: str) -> StoreServiceDto:
        service = self.get_service.get(id)
        questions = self.question_service.service_questions(service.id)
        return StoreServiceMapper.to_dto(service, questions)
    
    def filter(self, dto: FilterStoreServiceDto) -> List[StoreServiceDto]:
        services = self.get_service.filter(
            expresion=dto.expresion,
            order_by=dto.order_by,
            offset=dto.offset,
            limit=dto.limit,
            direction=dto.order_direction
        )
        return [self.find(service.id) for service in services]
    
    def add_image(self, service_id: str, base64_image: str) -> StoreServiceDto:
        service = self.get_service.get(service_id)
        service.add_image(base64_image)
        service.save()
        return StoreServiceMapper.to_dto(service)
    
    def delete_image(self, service_id: str, image: str) -> StoreServiceDto:
        service = self.get_service.get(service_id)
        service.delete_image(image)
        service.save()
        return StoreServiceMapper.to_dto(service)