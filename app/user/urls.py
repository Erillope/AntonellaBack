from django.urls import path
from .views import AuthView, UserView, RoleView, UserRoleView

urlpatterns = [
    path('user/auth/', AuthView.as_view()),
    path('user/', UserView.as_view()),
    path('role/', RoleView.as_view()),
    path('user/role/', UserRoleView.as_view())
]