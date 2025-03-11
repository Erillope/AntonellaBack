from django.urls import path
from .views import AuthView, UserView, RoleView, UserRoleView, PasswordTokenApi, ResetPasswordApi, FilterUserView

urlpatterns = [
    path('user/auth/', AuthView.as_view()),
    path('user/', UserView.as_view()),
    path('user/filter/', FilterUserView.as_view()),
    path('role/', RoleView.as_view()),
    path('user/role/', UserRoleView.as_view()),
    path('user/password/token/', PasswordTokenApi.as_view()),
    path('user/password/reset/', ResetPasswordApi.as_view())
]