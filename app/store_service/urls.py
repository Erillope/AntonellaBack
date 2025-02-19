from django.urls import path
from .views import (StoreServiceView, StoreServiceImageView, StoreServiceFilterView, QuestionView,
                    QuestionChoiceView)

urlpatterns = [
    path('store_service/', StoreServiceView.as_view()),
    path('store_service/image/', StoreServiceImageView.as_view()),
    path('store_service/filter/', StoreServiceFilterView.as_view()),
    path('store_service/question/', QuestionView.as_view()),
    path('store_service/question/choice/', QuestionChoiceView.as_view()),
]