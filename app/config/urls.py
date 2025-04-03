from django.urls import path
from .views import CategoriesApiView, ProductTypesApiView

urlpatterns = [
    path('categories/', CategoriesApiView.as_view()),
    path('product_types/', ProductTypesApiView.as_view()),   
]