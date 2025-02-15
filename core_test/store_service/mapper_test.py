import unittest
from core.store_service.service.mapper import StoreServiceMapper, QuestionMapper
from core.store_service import FormQuestion, TextChoiceQuestion, ImageChoiceQuestion
from core.store_service.service.dto import QuestionInputType
from .test_data import DataFactory
from typing import cast

class StoreServiceMapperTest(unittest.TestCase):
    def test_to_store_service(self) -> None:
        for create_store_service_dto in DataFactory.generate_create_store_services_dto():
            with self.subTest():
                store_service = StoreServiceMapper.to_store_service(create_store_service_dto)
                self.assertEqual(create_store_service_dto.name.lower(), store_service.name)
                self.assertEqual(create_store_service_dto.description.lower(), store_service.description)
                self.assertEqual(create_store_service_dto.type, store_service.type)
                self.assertEqual(len(create_store_service_dto.images), len(store_service.images))
        
    def test_to_dto(self) -> None:
        for store_service in DataFactory.generate_store_services():
            with self.subTest(store_service=store_service):
                dto = StoreServiceMapper.to_dto(store_service)
                self.assertEqual(store_service.id, dto.id)
                self.assertEqual(store_service.name, dto.name.lower())
                self.assertEqual(store_service.description, dto.description.lower())
                self.assertEqual(store_service.type, dto.type)
                self.assertEqual(store_service.created_date, dto.created_date)
                self.assertEqual(store_service.status, dto.status)
                self.assertEqual(store_service.images, dto.images)


class QuestionMappertTest(unittest.TestCase):
    def test_to_form_question(self) -> None:
        for create_question_dto in DataFactory.generate_create_form_question_dto():
            with self.subTest():
                question = cast(FormQuestion, QuestionMapper.to_question(create_question_dto))
                self.assertIsInstance(question, FormQuestion)
                self.assertEqual(create_question_dto.title.lower(), question.title)
                self.assertEqual(create_question_dto.input_type.value, question.input_type.value)

    def test_to_text_choice(self) -> None:
        for create_question_dto in DataFactory.generate_create_text_choice_question_dto():
            with self.subTest():
                question = cast(TextChoiceQuestion, QuestionMapper.to_question(create_question_dto))
                self.assertIsInstance(question, TextChoiceQuestion)
                self.assertEqual(create_question_dto.title.lower(), question.title)
                self.assertEqual(len(create_question_dto.choices), len(question.choices))
    
    def test_to_image_choice(self) -> None:
        for create_question_dto in DataFactory.generate_create_image_choice_question_dto():
            with self.subTest():
                question = cast(ImageChoiceQuestion, QuestionMapper.to_question(create_question_dto))
                self.assertIsInstance(question, ImageChoiceQuestion)
                self.assertEqual(create_question_dto.title.lower(), question.title)
                self.assertEqual(len(create_question_dto.choices), len(question.choices))
    
    def test_to_dto_from_form_question(self) -> None:
        for form_question in DataFactory.generate_form_questions():
            with self.subTest():
                dto = QuestionMapper.to_dto(form_question)
                self.assertEqual(form_question.id, dto.id)
                self.assertEqual(form_question.title, dto.title.lower())
                self.assertEqual(form_question.input_type.value, dto.input_type.value)
    
    def test_to_dto_from_text_choice(self) -> None:
        for text_choice_question in DataFactory.generate_text_choice_questions():
            with self.subTest():
                dto = QuestionMapper.to_dto(text_choice_question)
                self.assertEqual(text_choice_question.id, dto.id)
                self.assertEqual(text_choice_question.title, dto.title.lower())
                self.assertEqual(dto.input_type, QuestionInputType.CHOICE)
                self.assertEqual(text_choice_question.choices, [choice.option for choice in dto.choices])
    
    def test_to_dto_from_image_choice(self) -> None:
        for image_choice_question in DataFactory.generate_image_choice_questions():
            with self.subTest():
                dto = QuestionMapper.to_dto(image_choice_question)
                self.assertEqual(image_choice_question.id, dto.id)
                self.assertEqual(image_choice_question.title, dto.title.lower())
                self.assertEqual(dto.input_type, QuestionInputType.CHOICE)
                self.assertEqual(len(image_choice_question.choices), len(dto.choices))
        