from core.product import ProductService
from .repository import DjangoGetProduct, DjangoSaveProduct, DjangoDeleteProduct

get_product = DjangoGetProduct()

save_product = DjangoSaveProduct()

delete_product = DjangoDeleteProduct()

product_service = ProductService(
    get_product=get_product
)