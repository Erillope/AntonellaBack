from abc import ABC, abstractmethod
from .dto import ProductDto, CreateProductDto, UpdateProductDto, ProductFilterDto, ProductFilterResponseDto
from typing import List

class AbstractProductService(ABC):
    @abstractmethod
    def create(self, dto: CreateProductDto) -> ProductDto: ...
    
    @abstractmethod
    def update(self, dto: UpdateProductDto) -> ProductDto: ...
    
    @abstractmethod
    def reduce_stock(self, product_id: str, quantity: int) -> ProductDto: ...
    
    @abstractmethod
    def get(self, product_id: str) -> ProductDto: ...
    
    @abstractmethod
    def delete(self, product_id: str) -> ProductDto: ...
    
    @abstractmethod
    def get_all(self) -> List[ProductDto]: ...
    
    @abstractmethod
    def filter(self, dto: ProductFilterDto) -> ProductFilterResponseDto: ...

    @abstractmethod
    def get_by_name(self, name: str) -> List[ProductDto]: ...