from pydantic import BaseModel
from core.store_service import ServiceType, ServiceStatus, Choice
from core.common import OrdenDirection
from typing import List, Optional
from datetime import date
from enum import Enum

class QuestionInputType(str, Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    CHOICE = 'CHOICE'


class ChoiceType(str, Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    VOID = 'VOID'


class CreateQuestionDto(BaseModel):
    title: str
    input_type: QuestionInputType
    choice_type: ChoiceType = ChoiceType.VOID
    choices: List[Choice] = []


class CreateStoreServiceDto(BaseModel):
    name: str
    description: str
    type: ServiceType
    images: List[str] = []
    questions: List[CreateQuestionDto] = []


class UpdateStoreServiceDto(BaseModel):
    id: str
    name: Optional[str]=None
    description: Optional[str]=None
    type: Optional[ServiceType]=None
    status: Optional[ServiceStatus]=None


class FilterStoreServiceDto(BaseModel):
    expresion: Optional[str] = None
    order_by: str
    offset: Optional[int] = None
    limit: Optional[int] = None
    order_direction: OrdenDirection = OrdenDirection.DESC


class QuestionDto(BaseModel):
    id: str
    title: str
    input_type: QuestionInputType
    choice_type: ChoiceType = ChoiceType.VOID
    choices: List[Choice] = []
       
class StoreServiceDto(BaseModel):
    id: str
    name: str
    description: str
    status: ServiceStatus
    type: ServiceType
    images: List[str] = []
    questions: List[QuestionDto]
    created_date: date