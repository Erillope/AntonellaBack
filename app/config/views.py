from typing import Any, Dict
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import success_response, validate
from core.common.config import AppConfig
from rest_framework import serializers
from app.user.config import ServiceConfig
from core.common.email import EmailMessage

class ConfigDataSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    iva = serializers.DecimalField(max_digits=5, decimal_places=2)
    payment_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    terminos = serializers.CharField()

    def get_data(self) -> Dict[str, Any]:
        data = self.validated_data
        return {
            "email": data.get("email"),
            "password": data.get("password"),
            "iva": float(data.get("iva", 0)),
            "payment_percentage": float(data.get("payment_percentage", 0)),
            "terminos": data.get("terminos", "")
        }

class ConfigApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        config_data = {
            "email": AppConfig.app_email(),
            "password": AppConfig.email_password(),
            "iva": AppConfig.iva(),
            "payment_percentage": AppConfig.payment_percentage(),
            "terminos": AppConfig.terminos()
        }
        return success_response(config_data)
    
    @validate(ConfigDataSerializer)
    def put(self, request: ConfigDataSerializer) -> Response:
        config_data = request.get_data()
        email = config_data['email']
        password = config_data['password']
        try:
            ServiceConfig.email_host.set_host(email, password)
            ServiceConfig.email_host.send_email(EmailMessage(
                subject="Configuración de antonella admin",
                body="Este correo ha sido asociado a la configuración de antonella admin.",
                to=email
            ))
        except Exception as e:
            return Response({"message": f"Error sending email: {str(e)}"}, status=400)
        AppConfig.set_config_data(config_data)
        return success_response({"message": "Configuration updated successfully"})
    

class CategoriesApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        categories_info = AppConfig.categories_subtypes()
        return success_response(categories_info)


class ProductTypesApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        product_types = AppConfig.producy_types()
        return success_response(product_types)