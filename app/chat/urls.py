from django.urls import path
from .views import ChatApiView, UserChatView, AdminChatView

urlpatterns = [
    path('', ChatApiView.as_view()),
    path('from_user/', UserChatView.as_view()),
    path('from_admin/', AdminChatView.as_view()),
]