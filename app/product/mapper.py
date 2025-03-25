from app.common.table_mapper import TableMapper
from .models import ProductTableData, ProductImage
from core.product import Product, ProductFactory

class ProductTableMapper(TableMapper[ProductTableData, Product]):
    def to_model(self, table: ProductTableData) -> Product:
        return ProductFactory.load(
            id=str(table.id),
            name=table.name,
            service_type=table.service_type,
            description=table.description,
            price=table.price,
            stock=table.stock,
            created_date=table.created_date,
            images=ProductImage.get_product_images(str(table.id))
        )
    
    def to_table(self, product: Product) -> ProductTableData:
        return ProductTableData(
            id=product.id,
            name=product.name,
            service_type=product.service_type,
            description=product.description,
            price=product.price,
            stock=product.stock,
            created_date=product.created_date
        )