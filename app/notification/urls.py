from django.urls import path
from .views import NotificationTokenView, NotificationView

urlpatterns = [
    path('token/', NotificationTokenView.as_view()),
    path('', NotificationView.as_view()),
]