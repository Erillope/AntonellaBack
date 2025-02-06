from core.user import AuthService, UpdateUserService, FilterUserService, UserAccount, Role, RoleService
from .models import UserAccountTableData, RoleTableData
from app.common.django_repository import DjangoGetModel, DjangoDeleteModel
from core.common import EventPublisher
from .mapper import UserTableMapper, RoleTableMapper
from .repository import DjangoSaveUser, DjangoSaveRole, RoleToUserSubscriber

user_mapper = UserTableMapper()

role_mapper = RoleTableMapper()

get_user = DjangoGetModel[UserAccountTableData, UserAccount](
    table=UserAccountTableData,
    mapper=user_mapper
)

save_user = DjangoSaveUser()

get_role = DjangoGetModel[RoleTableData, Role](
    table=UserAccountTableData,
    mapper=role_mapper
)

save_role = DjangoSaveRole()

delete_role = DjangoDeleteModel[RoleTableData, Role](
    table=UserAccountTableData,
    mapper=role_mapper
)

role_to_user_subscriber = RoleToUserSubscriber()

EventPublisher.subscribe(save_user)
EventPublisher.subscribe(save_role)
EventPublisher.subscribe(role_to_user_subscriber)

auth_service = AuthService(
    get_user=get_user
)

update_user_service = UpdateUserService(
    get_user=get_user
)

filter_user_service = FilterUserService(
    get_user=get_user
)

role_service = RoleService(
    get_role=get_role,
    delete_role=delete_role
)