from django.urls import path
from .views import NotificationTokenView

urlpatterns = [
    path('token/', NotificationTokenView.as_view()),
]