from django.urls import path
from .views import OrderApiView, ServiceItemApiView, ProductItemApiView, ServiceItemFilterApiView, EmployeeServiceInfoView

urlpatterns = [
    path('', OrderApiView.as_view()),
    path('service-item/', ServiceItemApiView.as_view()),
    path('product-item/', ProductItemApiView.as_view()),
    path('service-item/filter/', ServiceItemFilterApiView.as_view()),
    path('service-item/employee-info/', EmployeeServiceInfoView.as_view()),
]