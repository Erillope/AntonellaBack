from app.common.table_mapper import TableMapper
from core.publicidad.publicidad import Publicidad, PublicidadFactory
from .models import PublicidadTable, ServicePublicidad, ProductPublicidad, PublicidadImage
from core.publicidad.publicidad import ItemData

class PublicidadTableMapper(TableMapper[PublicidadTable, Publicidad]):
    def to_model(self, table: PublicidadTable) -> Publicidad:
        return PublicidadFactory.load(
            id=str(table.id),
            title=table.title,
            created_date=table.created_date,
            images=PublicidadImage.get_publicidad_images(str(table.id)),
            service_items=[
                ItemData(id=sp.id, discount=sp.discount)
                for sp in ServicePublicidad.get_publicidad_services(str(table.id))
            ],
            product_items=[
                ItemData(id=pp.id, discount=pp.discount)
                for pp in ProductPublicidad.get_publicidad_products(str(table.id))
            ],
            description=table.description
        )
    
    def to_table(self, publicidad: Publicidad) -> PublicidadTable:
        return PublicidadTable(
            id=publicidad.id,
            title=publicidad.title,
            created_date=publicidad.created_date,
            description=publicidad.description
        )