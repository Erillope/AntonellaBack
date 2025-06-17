from core.common.abstract_repository import GetModel
from ..domain.item import ServiceItem, ProductItem
from abc import ABC, abstractmethod
from typing import List

class GetServiceItem(GetModel[ServiceItem], ABC):
    @abstractmethod
    def get_by_order_id(self, order_id: str) -> List[ServiceItem]: ...


class GetProductItem(GetModel[ProductItem], ABC):
    @abstractmethod
    def get_by_order_id(self, order_id: str) -> List[ProductItem]: ...