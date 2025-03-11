from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from app.common.response import validate, success_response
from .config import TokenServiceConfig

class TokenView(APIView):
    token_service = TokenServiceConfig.token_service
    
    @validate()
    def get(self, request: Request) -> Response:
        token = self.token_service.get(request.GET.get('token_id'))
        return success_response(token.model_dump())