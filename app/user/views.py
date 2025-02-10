from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .config import auth_service, update_user_service, filter_user_service, role_service
from app.common.response import validate, success_response
from .serializer import (SignInSerializer, SignUpSerializer, UpdateUserSerializer, FilterUserSerializer,
                         AddRoleToUserSerializer)

class AuthView(APIView):
    @validate(SignInSerializer)
    def post(self, request: SignInSerializer) -> Response:
        user = auth_service.sign_in(**request.validated_data)
        return success_response(user.model_dump())


class UserView(APIView):
    @validate(SignUpSerializer)
    def post(self, request: SignUpSerializer) -> Response:
        user = auth_service.sign_up(request.to_dto())
        return success_response(user.model_dump())

    @validate(UpdateUserSerializer)
    def put(self, request: UpdateUserSerializer) -> Response:
        user = update_user_service.update_user(request.to_dto())
        return success_response(user.model_dump())

    def get(self, request: Request) -> Response:
        filter_serializer = FilterUserSerializer(data=request.GET)
        filter_serializer.is_valid(raise_exception=True)
        users = filter_user_service.filter_user(filter_serializer.to_dto())
        return success_response([user.model_dump() for user in users])


class RoleView(APIView):
    @validate()
    def get(self, request: Request) -> Response:
        roles = role_service.get_all()
        return success_response([role.model_dump() for role in roles])
    
    @validate()
    def post(self, request: Request) -> Response:
        role = role_service.create(request.GET.get('name'))
        return success_response(role.model_dump())

    @validate()
    def put(self, request: Request) -> Response:
        role = role_service.rename(request.GET.get('role'), request.GET.get('name'))
        return success_response(role.model_dump())
    
    @validate()
    def delete(self, request: Request) -> Response:
        role = role_service.delete(request.GET.get('role'))
        return success_response(role.model_dump())


class UserRoleView(APIView):
    @validate(AddRoleToUserSerializer)
    def post(self, request: AddRoleToUserSerializer) -> Response:
        data = request.validated_data
        data['user_id'] = str(data['user_id'])
        user = update_user_service.add_role(**data)
        return success_response(user.model_dump())

    @validate()
    def delete(self, request: Request) -> Response:
        user = update_user_service.remove_role(request.GET.get('user_id'), request.GET.get('role'))
        return success_response(user.model_dump())