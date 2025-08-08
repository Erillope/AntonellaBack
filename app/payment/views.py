from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from app.common.response import validate, success_response
from .paymentez_api import PaymentezApi
from .serializer import DebitPaymentSerializer, AddUserCardSerializer, AddUserCardWithCardIdSerializer
from app.order.config import order_service
from core.order.service.dto import UpdateOrderDto
from core.order.domain.values import OrderStatus, PaymentStatus, PaymentType

payment_service = PaymentezApi('NUVEISTG-EC-SERVER', 'Kn9v6ICvoRXQozQG2rK92WtjG6l08a')

class DebitPaymentView(APIView):    
    @validate(DebitPaymentSerializer)
    def post(self, request: DebitPaymentSerializer) -> Response:
        data = request.to_dto()
        payment_data = payment_service.debit(data)
        order_service.update_order(UpdateOrderDto(id=data.order_id, client_confirmed=OrderStatus.CONFIRMED,
                                                  payment_status=PaymentStatus.PAID, payment_type=PaymentType.CARD))
        return success_response(payment_data.model_dump())

class ListUserCardsView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)
        
        cards = payment_service.list_user_cards(user_id)
        return success_response([card.model_dump() for card in cards])
    
class AddUserCardView(APIView):
    @validate(AddUserCardSerializer)
    def post(self, request: AddUserCardSerializer) -> Response:
        card = payment_service.add_user_card(request.to_dto())
        return success_response(card.model_dump())


class AddUserCardWithCardIdView(APIView):
    @validate(AddUserCardWithCardIdSerializer)
    def post(self, request: AddUserCardWithCardIdSerializer) -> Response:
        payment_service.add_user_card_with_card_id(request.to_dto())
        return success_response({"message": "Card added successfully."})