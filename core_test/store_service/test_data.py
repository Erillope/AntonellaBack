import random
from core.store_service import (StoreServiceFactory, StoreService, ServiceType, InputType, Choice,
                                QuestionFactory, TextChoiceQuestion, ImageChoiceQuestion, FormQuestion,
                                ServiceStatus)
from core.store_service.domain.values import ServiceName, Price
from core_test.images_data import get_base64_string
from datetime import time
import lorem # type: ignore
from decimal import Decimal
from typing import Dict, Any

class StoreTestData:
    @classmethod
    def generate_store_service(cls) -> StoreService:
        return StoreServiceFactory.create(**cls.store_service_data())
    
    
    @classmethod
    def generate_form_question(cls) -> FormQuestion:
        return QuestionFactory.create_form_question(
            title=lorem.sentence(),
            input_type=random.choice(list(InputType))
        )
        
        
    @classmethod
    def generate_text_choice_question(cls) -> TextChoiceQuestion:
        return QuestionFactory.create_text_choice_question(
            title=lorem.sentence(),
            choices=[lorem.sentence() for _ in range(3)]
        )
    
    @classmethod
    def generate_image_choice_question(cls) -> ImageChoiceQuestion:
        return QuestionFactory.create_image_choice_question(
            title=lorem.sentence(),
            choices=[
                Choice(
                    option=lorem.sentence(),
                    image=get_base64_string()
                ) for _ in range(3)
            ]
        )
    
    @classmethod
    def store_service_data(cls) -> Dict[str, Any]:
        return {
            'name': ServiceName.MATCHER.generate(),
            'description': lorem.sentence(),
            'type': random.choice(list(ServiceType)),
            'duration': time(hour=random.randint(0, 23), minute=random.randint(0, 59)),
            'prices': [
                Price.build(
                    name=lorem.sentence(),
                    min=Decimal(random.randint(1, 100)),
                    max=Decimal(random.randint(101, 200))
                ) for _ in range(3)
            ],
            'images': [
                get_base64_string() for _ in range(3)
            ]
        }
        
    @classmethod
    def store_service_update_data(cls) -> Dict[str, Any]:
        return {
            'name': ServiceName.MATCHER.generate(),
            'description': lorem.sentence(),
            'type': random.choice(list(ServiceType)),
            'duration': time(hour=random.randint(0, 23), minute=random.randint(0, 59)),
            'prices': [
                Price.build(
                    name=lorem.sentence(),
                    min=Decimal(random.randint(1, 100)),
                    max=Decimal(random.randint(101, 200))
                ) for _ in range(3)
            ],
            'images': [
                get_base64_string() for _ in range(3)
            ],
            'status': random.choice(list(ServiceStatus))
        }