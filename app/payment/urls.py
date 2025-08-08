from django.urls import path
from .views import DebitPaymentView, AddUserCardView, ListUserCardsView

urlpatterns = [
    path('', ListUserCardsView.as_view()),
    path('debit/', DebitPaymentView.as_view()),
    path('add_card/', AddUserCardView.as_view()),
]