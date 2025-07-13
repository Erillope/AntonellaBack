from .abstract_services import AbstractProductService
from .dto import ProductDto, CreateProductDto, UpdateProductDto, ProductFilterDto, ProductFilterResponseDto
from .repository import GetProduct
from .mapper import ProductMapper
from ..domain import Product
from typing import List

class ProductService(AbstractProductService):
    def __init__(self, get_product: GetProduct) -> None:
        self.get_product = get_product
    
    def create(self, dto: CreateProductDto) -> ProductDto:
        product = ProductMapper.to_product(dto)
        product.save()
        return ProductMapper.to_dto(product)
    
    def update(self, dto: UpdateProductDto) -> ProductDto:
        product = self.get_product.get(dto.id)
        product.change_data(
            name=dto.name,
            service_type=dto.service_type,
            description=dto.description,
            price=dto.price,
            additional_stock=dto.additional_stock,
            images=dto.images,
            status=dto.status,
            service_subtype=dto.service_subtype,
            product_type=dto.product_type,
            volume=dto.volume,
        )
        product.save()
        return ProductMapper.to_dto(product)

    def reduce_stock(self, product_id: str, quantity: int) -> ProductDto:
        product = self.get_product.get(product_id)
        product.reduce_stock(quantity)
        product.save()
        return ProductMapper.to_dto(product)
    
    def delete(self, product_id: str) -> ProductDto:
        product = self.get_product.get(product_id)
        product.delete()
        return ProductMapper.to_dto(product)

    def get(self, product_id: str) -> ProductDto:
        product = self.get_product.get(product_id)
        return ProductMapper.to_dto(product)
    
    def get_all(self) -> List[ProductDto]:
        products = self.get_product.get_all()
        return [ProductMapper.to_dto(product) for product in products]

    def filter(self, dto: ProductFilterDto) -> ProductFilterResponseDto:
        total = self.get_product.total_count()
        products, filtered_count = self.get_product.get_filtered_products(dto)
        return ProductFilterResponseDto(
            total_count=total,
            filtered_count=filtered_count,
            products=[ProductMapper.to_dto(product) for product in products]
        )