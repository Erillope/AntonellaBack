from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .config import ServiceConfig
from app.common.response import validate, success_response, failure_response
from .serializer import (SignInSerializer, SignUpSerializer, UpdateUserSerializer, ResetPasswordSerializer, 
                         FilterUserSerializer, CreateRoleSerializer, UpdateRoleSerializer)
from core.common.email import EmailMessage
from random import randint

class AuthView(APIView):
    auth_service = ServiceConfig.auth_service
    
    @validate(SignInSerializer)
    def post(self, request: SignInSerializer) -> Response:
        user = self.auth_service.sign_in(**request.validated_data)
        return success_response(user.user_dump())


class UserView(APIView):
    auth_service = ServiceConfig.auth_service
    update_user_service = ServiceConfig.update_user_service
    filter_user_service = ServiceConfig.filter_user_service
    
    @validate(SignUpSerializer)
    def post(self, request: SignUpSerializer) -> Response:
        user = self.auth_service.sign_up(request.to_dto())
        return success_response(user.user_dump())

    @validate(UpdateUserSerializer)
    def put(self, request: UpdateUserSerializer) -> Response:
        user = self.update_user_service.update_user(request.to_dto())
        return success_response(user.user_dump())

    @validate()
    def get(self, request: Request) -> Response:
        user = self.filter_user_service.get_user(request.GET.get('user_id'))
        return success_response(user.user_dump())


class FilterUserView(APIView):
    filter_user_service = ServiceConfig.filter_user_service
    
    @validate()
    def get(self, request: Request) -> Response:
        filter_serializer = FilterUserSerializer(data=request.GET)
        if not filter_serializer.is_valid(): return failure_response(filter_serializer.errors)
        users = self.filter_user_service.filter_user(filter_serializer.to_dto())
        return success_response([user.user_dump() for user in users])


class RoleView(APIView):
    role_service = ServiceConfig.role_service
    
    @validate()
    def get(self, request: Request) -> Response:
        if request.GET.get('role'):
            role = self.role_service.get(request.GET.get('role'))
            return success_response(role.role_dump())
        roles = self.role_service.get_all()
        return success_response([role.role_dump() for role in roles])
    
    @validate(CreateRoleSerializer)
    def post(self, request: CreateRoleSerializer) -> Response:
        role = self.role_service.create(request.validated_data['name'], request.get_accesses())
        return success_response(role.role_dump())

    @validate(UpdateRoleSerializer)
    def put(self, request: UpdateRoleSerializer) -> Response:
        role = self.role_service.update(request.validated_data['role'], request.validated_data.get('name'), request.get_accesses())
        return success_response(role.role_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        role = self.role_service.delete(request.GET.get('role'))
        return success_response(role.role_dump())


class UserRoleView(APIView):
    update_user_service = ServiceConfig.update_user_service
    filter_user_service = ServiceConfig.filter_user_service
    
    @validate()
    def get(self, request: Request) -> Response:
        users = self.filter_user_service.get_by_role(request.GET.get('role'))
        return success_response([user.user_dump() for user in users])


class PasswordTokenApi(APIView):
    auth_service = ServiceConfig.auth_service
    
    @validate()
    def post(self, request: Request) -> Response:
        token = self.auth_service.create_change_password_token(request.GET.get('email'))
        return success_response(token.model_dump())


class PasswordCodeApi(APIView):
    user_service = ServiceConfig.filter_user_service
    email_host = ServiceConfig.email_host
    
    @validate()
    def post(self, request: Request) -> Response:
        email = request.GET.get('email').strip().lower()
        random_four_digit_code = str(randint(1000, 9999))
        user = self.user_service.get_user(user_id=email)
        self.email_host.send_email(EmailMessage(
            subject='Password Reset Code',
            to=email,
            body=f'Tu codigo para cambiar de contraseña es: {random_four_digit_code}'
        ))
        return success_response({'code': random_four_digit_code, 'user_id': user.id})

class ResetPasswordApi(APIView):
    update_user_service = ServiceConfig.update_user_service
    
    @validate(ResetPasswordSerializer)
    def post(self, request: ResetPasswordSerializer) -> Response:
        user = self.update_user_service.change_password_with_token(**request.validated_data)
        return success_response(user.user_dump())