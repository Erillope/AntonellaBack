from core.store_service import (StoreService, StoreServiceFactory, Question, QuestionFactory, InputType,
                                FormQuestion, TextChoiceQuestion, ImageChoiceQuestion)
from .dto import (CreateStoreServiceDto, StoreServiceDto, CreateQuestionDto, QuestionInputType,
                  QuestionDto, ChoiceType, ChoiceDto)
from typing import List, Optional
from core.common.image_storage import Base64ImageStorage
from core.common.config import MEDIA

class StoreServiceMapper:
    IMAGE_FOLDER = 'store_service'
    IMAGE_PATH = f'{MEDIA}/{IMAGE_FOLDER}'
    
    @classmethod
    def to_store_service(cls, dto: CreateStoreServiceDto) -> StoreService:
        store_service = StoreServiceFactory.create(
            name=dto.name,
            description=dto.description,
            type=dto.type
        )
        for base64_image in dto.images:
            image = Base64ImageStorage(folder=cls.IMAGE_PATH, base64_image=base64_image)
            store_service.add_image(image)
        return store_service
    
    @classmethod
    def to_dto(cls, service: StoreService, questions: Optional[List[QuestionDto]]=None) -> StoreServiceDto:
        return StoreServiceDto(
            id=service.id,
            name=service.name,
            description=service.description,
            status=service.status,
            type=service.type,
            images=service.images,
            questions=questions,
            created_date=service.created_date
        )


class QuestionMapper:
    IMAGE_FOLDER = 'choices'
    IMAGE_PATH = f'{MEDIA}/{IMAGE_FOLDER}'
    
    @classmethod
    def to_question(cls, dto: CreateQuestionDto) -> Question:
        if dto.input_type == QuestionInputType.CHOICE and dto.choice_type == ChoiceType.TEXT:
            return cls._to_text_choice(dto)
        if dto.input_type == QuestionInputType.CHOICE and dto.choice_type == ChoiceType.IMAGE:
            return cls._to_image_choice(dto)
        return cls._to_form_question(dto)
    
    @classmethod
    def to_dto(cls, question: Question) -> QuestionDto:
        question_dto : QuestionDto
        if isinstance(question, TextChoiceQuestion):
            question_dto = cls._to_dto_from_text_choice(question)
        if isinstance(question, ImageChoiceQuestion):
            question_dto = cls._to_dto_from_image_choice(question)
        if isinstance(question, FormQuestion):
            question_dto = cls._to_dto_from_form_question(question)
        return question_dto

    @classmethod
    def _to_text_choice(cls, dto: CreateQuestionDto) -> TextChoiceQuestion:
        question = QuestionFactory.create_text_choice_question(
                title=dto.title,
            )
        for choice in dto.choices:
            question.add_choice(choice.option)
        return question
    
    @classmethod
    def _to_image_choice(cls, dto: CreateQuestionDto) -> ImageChoiceQuestion:
        question = QuestionFactory.create_image_choice_question(
                title=dto.title,
            )
        for choice in dto.choices:
            image = Base64ImageStorage(folder=cls.IMAGE_PATH, base64_image=choice.image)
            question.add_choice(choice.option, image)
        return question
    
    @classmethod
    def _to_form_question(cls, dto: CreateQuestionDto) -> FormQuestion:
        return QuestionFactory.create_form_question(
            title=dto.title,
            input_type=InputType(dto.input_type.value)
        )
    
    @classmethod
    def _to_dto_from_form_question(cls, question: FormQuestion) -> QuestionDto:
        return QuestionDto(
            id=question.id,
            title=question.title,
            input_type=QuestionInputType(question.input_type.value)
        )
    
    @classmethod
    def _to_dto_from_text_choice(cls, question: TextChoiceQuestion) -> QuestionDto:
        return QuestionDto(
            id=question.id,
            title=question.title,
            input_type=QuestionInputType.CHOICE,
            choice_type=ChoiceType.TEXT,
            choices = [ChoiceDto(option=option) for option in question.choices]
        )
    
    @classmethod
    def _to_dto_from_image_choice(cls, question: ImageChoiceQuestion) -> QuestionDto:
        return QuestionDto(
            id=question.id,
            title=question.title,
            input_type=QuestionInputType.CHOICE,
            choice_type=ChoiceType.IMAGE,
            choices = [ChoiceDto(option=choice.option, image=choice.image.get_url())
                       for choice in question.choices]
        )