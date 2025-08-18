from django.urls import path
from .views import PublicidadApiView, RelatedPublicidadApiView, AddPublicidadToServiceApiView, FilterPublicidadApiView

urlpatterns = [
    path('', PublicidadApiView.as_view()),
    path('related/', RelatedPublicidadApiView.as_view()),
    path('add-to-item/', AddPublicidadToServiceApiView.as_view()),
    path('filter/', FilterPublicidadApiView.as_view()),
]