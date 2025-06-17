from django.urls import path
from .views import PublicidadApiView

urlpatterns = [
    path('', PublicidadApiView.as_view()),
]