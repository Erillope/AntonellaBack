from django.urls import path
from .views import DebitPaymentView, AddUserCardView

urlpatterns = [
    path('debit/', DebitPaymentView.as_view()),
    path('add_card/', AddUserCardView.as_view()),
]