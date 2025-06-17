from core.publicidad.publicidad_service import PublicidadService
from .repository import DjangoGetPublicidad, DjangoSavePublicidad, DjangoDeletePublicidad

get_publicidad = DjangoGetPublicidad()

save_publicidad = DjangoSavePublicidad()

delete_publicidad = DjangoDeletePublicidad()

publicidad_service = PublicidadService(
    get_publicidad=get_publicidad
)