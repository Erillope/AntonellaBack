from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate, failure_response
from .config import publicidad_service
from .serializer import CreatePublicidadSerializer, UpdatePublicidadSerializer, RelatedPublicidadSerializer, AddPublicidadToItemSerializer
from .models import SelectedPublicidad

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


class RelatedPublicidadApiView(APIView):
    @validate(RelatedPublicidadSerializer)
    def post(self, request: RelatedPublicidadSerializer) -> Response:
        related_publicidad = publicidad_service.get_related_publicidad(
            services_id=request.get_services_id(),
            products_id=request.get_products_id()
        )
        return success_response([pub.model_dump() for pub in related_publicidad])


class AddPublicidadToServiceApiView(APIView):
    @validate(AddPublicidadToItemSerializer)
    def post(self, request: AddPublicidadToItemSerializer) -> Response:
        data = request.validated_data
        service_id = data.get('service_id')
        product_id = data.get('product_id')
        publicidad_id = data['publicidad_id']

        if not service_id and not product_id:
            return Response({
                "status": "failure",
                "code": 400,
                "message": "Debes proporcionar al menos un servicio o producto."
            }, status=400)

        SelectedPublicidad.objects.create(
            publicidad_id=publicidad_id,
            service_item_id=service_id
        )
        return success_response({"message": "Publicidad added to item successfully."})