from .dto import CreateProductDto, ProductDto
from ..domain import Product, ProductFactory

class ProductMapper:
    @classmethod
    def to_product(cls, dto: CreateProductDto) -> Product:
        return ProductFactory.create(
            name=dto.name,
            service_type=dto.service_type,
            description=dto.description,
            price=dto.price,
            stock=dto.stock,
            images=dto.images
        )
    
    @classmethod
    def to_dto(cls, product: Product) -> ProductDto:
        return ProductDto(
            id=product.id,
            name=product.name,
            service_type=product.service_type,
            description=product.description,
            price=product.price,
            stock=product.stock,
            images=product.images,
            status=product.status
        )