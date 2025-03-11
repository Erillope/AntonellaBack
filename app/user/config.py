from core.user import AuthService, UpdateUserService, FilterUserService, RoleService
from .repository import (DjangoSaveUser, DjangoSaveRole, RoleToUserSubscriber,
                         DjangoGetRole, DjangoGetUser, DjangoDeleteRole)
from app.common.email import DjangoEmailHost
from app.tokens.repository import DjangoGetToken
from core.token import TokenService

class ServiceConfig:
    get_user = DjangoGetUser()
    save_user = DjangoSaveUser()
    get_role = DjangoGetRole()
    save_role = DjangoSaveRole()
    delete_role = DjangoDeleteRole()
    role_to_user_subscriber = RoleToUserSubscriber()
    token_service = TokenService(get_token=DjangoGetToken())
    auth_service = AuthService(
        get_user=get_user,
        get_role=get_role,
        token_service=token_service,
        email_host=DjangoEmailHost(),
    )
    update_user_service = UpdateUserService(
        get_user=get_user,
        get_role=get_role,
        token_service=token_service
    )
    filter_user_service = FilterUserService(
        get_user=get_user
    )
    role_service = RoleService(
        get_role=get_role
    )

    @classmethod
    def init(cls) -> None:
        cls.role_service.init()
        cls.auth_service.init()