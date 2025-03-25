from django.urls import path
from .views import ProductApiView

urlpatterns = [
    path('/', ProductApiView.as_view()),
]