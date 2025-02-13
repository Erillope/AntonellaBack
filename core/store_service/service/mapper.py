from core.store_service import (StoreService, StoreServiceFactory, Question, QuestionFactory, InputType,
                                FormQuestion, TextChoiceQuestion, ImageChoiceQuestion, Choice)
from .dto import CreateStoreServiceDto, StoreServiceDto, CreateQuestionDto, QuestionInputType, QuestionDto, ChoiceType
from typing import List

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
    def to_dto(service: StoreService, questions: List[QuestionDto]) -> StoreServiceDto:
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
            question.add_choice(choice)
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
            choices = [Choice(option=option) for option in question.choices]
        )
    
    @classmethod
    def _to_dto_from_image_choice(cls, question: ImageChoiceQuestion) -> QuestionDto:
        return QuestionDto(
            id=question.id,
            title=question.title,
            input_type=QuestionInputType.CHOICE,
            choice_type=ChoiceType.IMAGE,
            choices = question.choices
        )