from core_test.store_service.test_data import StoreTestData as CoreStoreTestData
from typing import Dict, Any
from core.store_service.service.dto import QuestionInputType, ChoiceType
from core_test.images_data import get_base64_string
from typing import List, Optional

class StoreTestData(CoreStoreTestData):
    @classmethod
    def generate_create_form_question_request(cls, service_id: Optional[str]=None) -> Dict[str, Any]:
        question = cls.generate_form_question()
        data = {
            'title': question.title,
            'input_type': question.input_type.value
        }
        if service_id: data['service_id'] = service_id
        return data
    
    @classmethod
    def generate_create_text_choice_question_request(cls, service_id: Optional[str]=None) -> Dict[str, Any]:
        question = cls.generate_text_choice_question()
        data = {
            'title': question.title,
            'input_type': QuestionInputType.CHOICE.value,
            'choice_type': ChoiceType.TEXT.value,
            'choices': [choice for choice in question.choices]
        }
        if service_id: data['service_id'] = service_id
        return data
        
    @classmethod
    def generate_create_image_choice_question_request(cls, service_id: Optional[str]=None) -> Dict[str, Any]:
        question = cls.generate_image_choice_question()
        data = {
            'title': question.title,
            'input_type': QuestionInputType.CHOICE.value,
            'choice_type': ChoiceType.IMAGE.value,
            'choices': [
                {
                    'option': choice.option,
                    'image': get_base64_string()
                }
                for choice in question.choices
            ]
        }
        if service_id: data['service_id'] = service_id
        return data
    
    @classmethod
    def generate_create_service_request(cls, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        service = cls.generate_store_service()
        return {
            'name': service.name,
            'description': service.description,
            'type': service.type.value,
            'subtype': service.subtype,
            'duration': service.duration.isoformat(),
            'prices': [
                {
                    'name': price.name,
                    'min_price': float(price.range.min),
                    'max_price': float(price.range.max)
                } for price in service.prices
            ],
            'images': [get_base64_string() for _ in range(3)],
            'questions': questions
        }
    
    @classmethod
    def generate_update_service_request(cls, service_id: str) -> Dict[str, Any]:
        service = cls.generate_store_service()
        return {
            'id': service_id,
            'name': service.name,
            'description': service.description,
            'type': service.type.value,
            'subtype': service.subtype,
            'duration': service.duration.isoformat(),
            'prices': [
                {
                    'name': price.name,
                    'min_price': float(price.range.min),
                    'max_price': float(price.range.max)
                } for price in service.prices
            ],
            'images': [get_base64_string() for _ in range(3)]
        }