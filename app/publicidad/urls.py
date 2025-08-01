from django.urls import path
from .views import PublicidadApiView, RelatedPublicidadApiView, AddPublicidadToServiceApiView

urlpatterns = [
    path('', PublicidadApiView.as_view()),
    path('related/', RelatedPublicidadApiView.as_view()),
    path('add-to-item/', AddPublicidadToServiceApiView.as_view()),
]