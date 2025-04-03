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
            images=dto.images,
            service_subtype=dto.service_subtype,
            product_type=dto.product_type,
            volume=dto.volume
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
            status=product.status,
            service_subtype=product.service_subtype,
            product_type=product.product_type,
            volume=product.volume,
            stock_modified_date=product.stock_modified_date,
            created_date=product.created_date,
        )