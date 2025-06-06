from core.common.abstract_repository import GetModel
from ..domain.item import ServiceItem
from abc import ABC, abstractmethod
from typing import List

class GetServiceItem(GetModel[ServiceItem], ABC):
    @abstractmethod
    def get_by_order_id(self, order_id: str) -> List[ServiceItem]: ...