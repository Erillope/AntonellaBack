import json
from typing import List, Dict, Any, Optional
import random
from core.store_service import (StoreServiceFactory, StoreService, ServiceType, ServiceStatus, InputType,
                                QuestionFactory, TextChoiceQuestion, ImageChoiceQuestion, FormQuestion)
from core.store_service.service.dto import (CreateStoreServiceDto, CreateQuestionDto, QuestionInputType,
                                            ChoiceType, ChoiceDto)
from core_test.images_data import get_base64_strings
from core.common.config import MEDIA
from core.common import ID
import lorem

class StoreTestData:
    instance: Optional['StoreTestData'] = None
    BASE64_IMAGES = get_base64_strings()
    
    def __init__(self) -> None:
        self.data: Dict[str, List[Any]] = {}
        with open('core_test/store_service/store_service_test_data.json', encoding='utf-8') as file:
            self.data = json.load(file)
        self.shuffle()
    
    def shuffle(self) -> None:
        for key in self.data:
            random.shuffle(self.data[key])
    
    @classmethod      
    def get_instance(cls) -> 'StoreTestData':
        if cls.instance is None:
            cls.instance = StoreTestData()
        return cls.instance
    
    def get_names(self) -> List[str]:
        return self.data['names']
    
    def get_invalid_names(self) -> List[str]:
        return self.data['invalid_names']
    
    def get_service_type(self) -> ServiceType:
        return random.choice(list(ServiceType))
    
    def get_service_status(self) -> ServiceStatus:
        return random.choice(list(ServiceStatus))
    
    def get_description(self) -> str:
        text: str = lorem.sentence()
        return text
    
    def get_sample_base64_images(self) -> List[str]:
        return random.sample(self.BASE64_IMAGES, random.randint(1, len(self.BASE64_IMAGES)))
    
    def get_input_type(self) -> InputType:
        return random.choice(list(InputType))

    def get_question_input_type(self) -> QuestionInputType:
        return random.choice(list(QuestionInputType))
    
    def generate_image_url(self) -> str:
        return f'{MEDIA}/{ID.generate()}.png'


class DataFactory:
    store_test_data: StoreTestData = StoreTestData.get_instance()
    
    @classmethod
    def generate_store_services(cls) -> List[StoreService]:
        return [
            StoreServiceFactory.create(
                name=name,
                description=cls.store_test_data.get_description(),
                type=cls.store_test_data.get_service_type(),
            )
            for name in cls.store_test_data.get_names()
        ]
    
    @classmethod
    def generate_create_store_services_dto(cls) -> List[CreateStoreServiceDto]:
        return [
            CreateStoreServiceDto(
                name=name,
                description=cls.store_test_data.get_description(),
                type=cls.store_test_data.get_service_type()
                )
            for name in cls.store_test_data.get_names()
        ]
    
    @classmethod
    def generate_form_questions(cls) -> List[FormQuestion]:
        return [
            QuestionFactory.create_form_question(title=cls.store_test_data.get_description(),
                                                 input_type=cls.store_test_data.get_input_type())
            for _ in range(10)
        ]
        
    @classmethod
    def generate_text_choice_questions(cls) -> List[TextChoiceQuestion]:
        return [
            QuestionFactory.create_text_choice_question(title=cls.store_test_data.get_description())
            for _ in range(10)
        ]
    
    @classmethod
    def generate_image_choice_questions(cls) -> List[ImageChoiceQuestion]:
        return [
            QuestionFactory.create_image_choice_question(title=cls.store_test_data.get_description())
            for _ in range(10)
        ]
    
    @classmethod
    def generate_create_form_question_dto(cls) -> List[CreateQuestionDto]:
        return [
            CreateQuestionDto(
                title=cls.store_test_data.get_description(),
                input_type=random.choice([QuestionInputType.TEXT, QuestionInputType.IMAGE])
            )
            for _ in range(10)
        ]
    
    @classmethod
    def generate_create_text_choice_question_dto(cls) -> List[CreateQuestionDto]:
        return [
            CreateQuestionDto(
                title=cls.store_test_data.get_description(),
                input_type=QuestionInputType.CHOICE,
                choice_type=ChoiceType.TEXT,
                choices=[ChoiceDto(option=cls.store_test_data.get_description()) for _ in range(3)]
            )
            for _ in range(10)
        ]
    
    @classmethod
    def generate_create_image_choice_question_dto(cls) -> List[CreateQuestionDto]:
        return [
            CreateQuestionDto(
                title=cls.store_test_data.get_description(),
                input_type=QuestionInputType.CHOICE,
                choice_type=ChoiceType.IMAGE,
                choices=[ChoiceDto(option=cls.store_test_data.get_description(), image=cls.store_test_data.generate_image_url())
                         for _ in range(3)]
            )
            for _ in range(10)
        ]