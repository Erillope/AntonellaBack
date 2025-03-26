from django.urls import path
from .views import (StoreServiceView, QuestionView)

urlpatterns = [
    path('', StoreServiceView.as_view()),
    path('question/', QuestionView.as_view()),
]