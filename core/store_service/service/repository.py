from core.common.abstract_repository import GetModel
from core.store_service import Question
from abc import ABC, abstractmethod
from typing import List

class GetQuestion(GetModel[Question], ABC):
    @abstractmethod
    def get_service_questions(self, service_id: str) -> List[Question]: ...