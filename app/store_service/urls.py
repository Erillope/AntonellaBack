from django.urls import path
from .views import (StoreServiceView, QuestionView)

urlpatterns = [
    path('store_service/', StoreServiceView.as_view()),
    path('store_service/question/', QuestionView.as_view()),
]