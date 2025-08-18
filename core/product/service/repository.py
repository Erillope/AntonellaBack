from abc import ABC, abstractmethod
from .dto import ProductFilterDto
from core.common.abstract_repository import GetModel
from ..domain import Product
from typing import List, Tuple

class GetProduct(GetModel[Product], ABC):
    @abstractmethod
    def get_filtered_products(self, dto: ProductFilterDto) -> Tuple[List[Product], int]: ...

    @abstractmethod
    def get_by_name(self, name: str) -> List[Product]: ...