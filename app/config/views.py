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
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)
    iva = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    payment_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    terminos = serializers.CharField(required=False)
    salario = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    def get_data(self) -> Dict[str, Any]:
        data = self.validated_data
        return {
            "email": data.get("email"),
            "password": data.get("password"),
            "iva": float(data.get("iva")) if data.get("iva") else None,
            "payment_percentage": float(data.get("payment_percentage")) if data.get("payment_percentage") else None,
            "terminos": data.get("terminos"),
            "salario": float(data.get("salario")) if data.get("salario") else None
        }

class ConfigApiView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        config_data = {
            "email": AppConfig.app_email(),
            "password": AppConfig.email_password(),
            "iva": AppConfig.iva(),
            "payment_percentage": AppConfig.payment_percentage(),
            "terminos": AppConfig.terminos(),
            "salario": AppConfig.salario()
        }
        return success_response(config_data)
    
    @validate(ConfigDataSerializer)
    def put(self, request: ConfigDataSerializer) -> Response:
        config_data = request.get_data()
        email = config_data.get('email')
        password = config_data.get('password')
        now_email = ServiceConfig.email_host.email_host
        now_password = ServiceConfig.email_host.password
        try:
            if email and password:
                ServiceConfig.email_host.set_host(email, password)
            if email:
                ServiceConfig.email_host.set_host(email, now_password)
            if password:
                ServiceConfig.email_host.set_host(now_email, password)
            email_changed = isinstance(email, str) and email.lower() != now_email.lower()
            password_changed = isinstance(password, str) and password != now_password
            if email_changed or password_changed:
                ServiceConfig.email_host.send_email(EmailMessage(
                    subject="Configuración de antonella admin",
                    body="Este correo ha sido asociado a la configuración de antonella admin.",
                    to=email if email else now_email
                ))
        except Exception as e:
            ServiceConfig.email_host.set_host(now_email, now_password)
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
        product_types = AppConfig.product_types()
        return success_response(product_types)