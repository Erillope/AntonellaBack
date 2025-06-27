from django.urls import path
from .views import (StoreServiceView, QuestionView, FilterStoreServiceView)

urlpatterns = [
    path('', StoreServiceView.as_view()),
    path('filter/', FilterStoreServiceView.as_view()),
    path('question/', QuestionView.as_view()),
]