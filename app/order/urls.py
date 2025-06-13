from django.urls import path
from .views import OrderApiView, ServiceItemApiView

urlpatterns = [
    path('', OrderApiView.as_view()),
    path('service-item/', ServiceItemApiView.as_view()),
]