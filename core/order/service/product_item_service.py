from abc import ABC, abstractmethod
from .dto import ProductItemDto, UpdateProductItemDto
from .repository import GetProductItem
from .mapper import ProductItemMapper
from core.product.service import AbstractProductService
from typing import List

class AbstractProductItemService(ABC):
    @abstractmethod
    def get_product_items(self, order_id: str) -> List[ProductItemDto]: ...

    @abstractmethod
    def create_product_item(self, dto: ProductItemDto, order_id: str) -> ProductItemDto: ...

    @abstractmethod
    def update_product_item(self, dto: UpdateProductItemDto) -> ProductItemDto: ...

    @abstractmethod
    def delete_product_item(self, product_item_id: str) -> None: ...


class ProductItemService(AbstractProductItemService):
    def __init__(self, get_product_item: GetProductItem, product_service: AbstractProductService) -> None:
        self._get_product_item = get_product_item
        self._product_service = product_service
    
    def get_product_items(self, order_id: str) -> List[ProductItemDto]:
        product_items = self._get_product_item.get_by_order_id(order_id)
        return [ProductItemMapper.to_product_item_dto(item) for item in product_items]
    
    def create_product_item(self, dto: ProductItemDto, order_id: str) -> ProductItemDto:
        product_item = ProductItemMapper.to_product_item(dto)
        product_item.set_order_id(order_id)
        product_item.save()
        self._product_service.reduce_stock(product_id=dto.product_id, quantity=dto.quantity)
        return ProductItemMapper.to_product_item_dto(product_item)
    
    def update_product_item(self, dto: UpdateProductItemDto) -> ProductItemDto:
        product_item = self._get_product_item.get(dto.id)
        product_item.update_data(
            product_id=dto.product_id,
            quantity=dto.quantity,
            base_price=dto.base_price
        )
        product_item.save()
        return ProductItemMapper.to_product_item_dto(product_item)
    
    def delete_product_item(self, product_item_id: str) -> None:
        product_item = self._get_product_item.get(product_item_id)
        product_item.delete()
        return None