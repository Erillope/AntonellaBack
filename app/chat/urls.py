from django.urls import path
from .views import ChatApiView, UserChatView, AdminChatView, AdminReadChatView, AdminReadChatMessageView

urlpatterns = [
    path('', ChatApiView.as_view()),
    path('from_user/', UserChatView.as_view()),
    path('from_admin/', AdminChatView.as_view()),
    path('admin/read/', AdminReadChatView.as_view()),
    path('admin/read/message/', AdminReadChatMessageView.as_view()),
]