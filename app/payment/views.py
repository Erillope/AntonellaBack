from rest_framework.views import APIView
from rest_framework.response import Response
from app.common.response import validate, success_response
from .paymentez_api import PaymentezApi
from .serializer import DebitPaymentSerializer, AddUserCardSerializer, AddUserCardWithCardIdSerializer

payment_service = PaymentezApi('NUVEISTG-EC-SERVER', 'Kn9v6ICvoRXQozQG2rK92WtjG6l08a')

class DebitPaymentView(APIView):    
    @validate(DebitPaymentSerializer)
    def post(self, request: DebitPaymentSerializer) -> Response:
        payment_data = payment_service.debit(request.to_dto())
        return success_response(payment_data.model_dump())


class AddUserCardView(APIView):
    @validate(AddUserCardSerializer)
    def post(self, request: AddUserCardSerializer) -> Response:
        payment_service.add_user_card(request.to_dto())
        return success_response({"message": "Card added successfully"})


class AddUserCardWithCardIdView(APIView):
    @validate(AddUserCardWithCardIdSerializer)
    def post(self, request: AddUserCardWithCardIdSerializer) -> Response:
        payment_service.add_user_card_with_card_id(request.to_dto())
        return success_response({"message": "Card added successfully with card ID"})