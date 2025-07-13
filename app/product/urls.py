from django.urls import path
from .views import ProductApiView, ProductFilterApiView

urlpatterns = [
    path('', ProductApiView.as_view()),
    path('filter/', ProductFilterApiView.as_view()),
]