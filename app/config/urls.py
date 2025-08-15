from django.urls import path
from .views import CategoriesApiView, ProductTypesApiView, ConfigApiView

urlpatterns = [
    path('', ConfigApiView.as_view()),
    path('categories/', CategoriesApiView.as_view()),
    path('product_types/', ProductTypesApiView.as_view()),   
]