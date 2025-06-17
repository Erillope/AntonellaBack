from django.urls import path
from .views import OrderApiView, ServiceItemApiView, ProductItemApiView

urlpatterns = [
    path('', OrderApiView.as_view()),
    path('service-item/', ServiceItemApiView.as_view()),
    path('product-item/', ProductItemApiView.as_view()),
]