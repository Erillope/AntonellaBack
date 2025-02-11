from django.urls import path
from .views import StoreServiceView, StoreServiceImageView, StoreServiceFilterView

urlpatterns = [
    path('store_service/', StoreServiceView.as_view()),
    path('store_service/image/', StoreServiceImageView.as_view()),
    path('store_service/filter/', StoreServiceFilterView.as_view())
]