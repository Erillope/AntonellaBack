from django.urls import path
from .views import AnswerApiView

urlpatterns = [
    path('', AnswerApiView.as_view()),
]