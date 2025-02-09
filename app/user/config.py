from core.user import AuthService, UpdateUserService, FilterUserService, Role, RoleService
from .models import UserAccountTableData, RoleTableData
from app.common.django_repository import DjangoDeleteModel
from .mapper import UserTableMapper, RoleTableMapper
from .repository import DjangoSaveUser, DjangoSaveRole, RoleToUserSubscriber, DjangoGetRole, DjangoGetUser

user_mapper = UserTableMapper()

role_mapper = RoleTableMapper()

get_user = DjangoGetUser()

save_user = DjangoSaveUser()

get_role = DjangoGetRole()

save_role = DjangoSaveRole()

delete_role = DjangoDeleteModel[RoleTableData, Role](
    table=UserAccountTableData,
    mapper=role_mapper,
    get_model=get_role
)

role_to_user_subscriber = RoleToUserSubscriber()

auth_service = AuthService(
    get_user=get_user,
    get_role=get_role
)

update_user_service = UpdateUserService(
    get_user=get_user,
    get_role=get_role
)

filter_user_service = FilterUserService(
    get_user=get_user
)

role_service = RoleService(
    get_role=get_role
)