from django.urls import path
from .views import (StoreServiceView, QuestionView, FilterStoreServiceView, FilterStoreServiceV2View)

urlpatterns = [
    path('', StoreServiceView.as_view()),
    path('filter/', FilterStoreServiceView.as_view()),
    path('question/', QuestionView.as_view()),
    path('filter-v2/', FilterStoreServiceV2View.as_view()),
]