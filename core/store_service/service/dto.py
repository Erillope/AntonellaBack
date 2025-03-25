from pydantic import BaseModel
from core.store_service import ServiceType, ServiceStatus
from core.store_service.domain.values import Price
from core.common import OrdenDirection
from typing import List, Optional, Dict, Any
from datetime import date, time
from enum import Enum

class QuestionInputType(str, Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    CHOICE = 'CHOICE'


class ChoiceType(str, Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    VOID = 'VOID'


class ChoiceDto(BaseModel):
    option: str
    image: str = ''
    
    
class CreateQuestionDto(BaseModel):
    title: str
    input_type: QuestionInputType
    choice_type: ChoiceType = ChoiceType.VOID
    choices: List[ChoiceDto] = []


class CreateStoreServiceDto(BaseModel):
    name: str
    description: str
    type: ServiceType
    duration: time
    prices: List[Price]
    images: List[str] = []
    questions: List[CreateQuestionDto]


class UpdateStoreServiceDto(BaseModel):
    id: str
    name: Optional[str]=None
    description: Optional[str]=None
    type: Optional[ServiceType]=None
    duration: Optional[time]=None
    prices: Optional[List[Price]]=None
    images: Optional[List[str]]=None
    status: Optional[ServiceStatus]=None


class FilterStoreServiceDto(BaseModel):
    order_by: str
    offset: Optional[int] = None
    limit: Optional[int] = None
    order_direction: OrdenDirection = OrdenDirection.DESC


class QuestionDto(BaseModel):
    id: str
    title: str
    input_type: QuestionInputType
    choice_type: ChoiceType = ChoiceType.VOID
    choices: List[ChoiceDto] = []
    
    def question_dump(self) -> Dict[str, Any]:
        data = self.model_dump()
        if self.choice_type == ChoiceType.VOID:
            data.pop('choices')
            data.pop('choice_type')
        if self.choice_type == ChoiceType.TEXT:
            data['choices'] = [choice.option for choice in self.choices]
        return data
       
class StoreServiceDto(BaseModel):
    id: str
    name: str
    description: str
    status: ServiceStatus
    type: ServiceType
    duration: time
    prices: List[Price]
    images: List[str] = []
    questions: Optional[List[QuestionDto]] = None
    created_date: date
    
    def service_dump(self) -> Dict[str, Any]:
        data = self.model_dump()
        if self.questions:
            data['questions'] = [question.question_dump() for question in self.questions]
        else:
            data.pop('questions')
        return data