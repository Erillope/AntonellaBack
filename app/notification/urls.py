from django.urls import path
from .views import NotificationTokenView, NotificationView, NotificationFilterView

urlpatterns = [
    path('token/', NotificationTokenView.as_view()),
    path('', NotificationView.as_view()),
    path('filter/', NotificationFilterView.as_view()),
]