from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from .config import publicidad_service
from .serializer import CreatePublicidadSerializer, UpdatePublicidadSerializer

class PublicidadApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        if request.GET.get('id'):
            publicidad = publicidad_service.get_publicidad(request.GET.get('id'))
            return success_response(publicidad.model_dump())
        else:
            publicidades = publicidad_service.get_all()
            return success_response([publicidad.model_dump() for publicidad in publicidades])
    
    @validate(CreatePublicidadSerializer)
    def post(self, request: CreatePublicidadSerializer) -> Response:
        publicidad = publicidad_service.create_publicidad(request.to_dto())
        return success_response(publicidad.model_dump())
    
    @validate(UpdatePublicidadSerializer)
    def put(self, request: UpdatePublicidadSerializer) -> Response:
        publicidad = publicidad_service.update_publicidad(request.to_dto())
        return success_response(publicidad.model_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        publicidad_service.delete_publicidad(request.GET.get('id'))
        return success_response({"message": "Publicidad deleted successfully."})