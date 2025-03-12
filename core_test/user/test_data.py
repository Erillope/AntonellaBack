from core_test.images_data import get_base64_string
from core.common import ID
from core.user import AccountStatus, Gender, UserAccount, UserAccountFactory, RoleFactory, Role, EmployeeAccount
from core.user.domain.values import UserName, UserEmail, UserPassword, UserPhoneNumber, UserBirthdate, DniValue, RoleAccess, AccessType, PermissionType
import random
from datetime import date, timedelta

class UserDataFactory:
    @classmethod
    def generate_user_account(cls) -> UserAccount:
        return UserAccountFactory.load_user(
            id=ID.generate(),
            name=UserName.MATCHER.generate(),
            email=UserEmail.MATCHER.generate(),
            password=UserPassword.MATCHER.generate(),
            phone_number=UserPhoneNumber.MATCHER.generate(),
            birthdate=cls.get_birthdate(),
            status=random.choice(list(AccountStatus)),
            gender=random.choice(list(Gender)),
            created_date=cls.get_created_date(),
        )
    
    @classmethod
    def generate_employee_account(cls) -> EmployeeAccount:
        return UserAccountFactory.load_employee(
            id=ID.generate(),
            name=UserName.MATCHER.generate(),
            email=UserEmail.MATCHER.generate(),
            password=UserPassword.MATCHER.generate(),
            phone_number=UserPhoneNumber.MATCHER.generate(),
            birthdate=cls.get_birthdate(),
            status=random.choice(list(AccountStatus)),
            gender=random.choice(list(Gender)),
            created_date=cls.get_created_date(),
            dni=DniValue.MATCHER.generate(),
            address=UserName.MATCHER.random(50),
            photo=get_base64_string(),
            roles=[Role.MATCHER.generate() for _ in range(random.randint(1, 5))],
        )
    
    @classmethod
    def generate_role(cls) -> Role:
        return RoleFactory.load(
            id=ID.generate(),
            name=Role.MATCHER.generate(),
            accesses={cls.generate_role_access() for _ in range(random.randint(1, 5))},
            created_date=cls.get_created_date(),
        )
    
    @classmethod
    def generate_role_access(cls) -> RoleAccess:
        return RoleAccess(
            access_type=random.choice(list(AccessType)),
            permissions=set(random.sample(list(PermissionType), random.randint(1, 4))),
        )
    
    
    @classmethod
    def get_birthdate(cls) -> date:
        start_date = date(date.today().year - UserBirthdate.MAX_AGE + 1, date.today().month, date.today().day)
        end_date = date(date.today().year - UserBirthdate.MIN_AGE - 1, date.today().month, date.today().day)
        delta = end_date - start_date
        return start_date + timedelta(days=random.randint(0, delta.days))
    
    @classmethod
    def get_invalid_birthdate(cls) -> date:
        start_date = date(date.today().year - UserBirthdate.MAX_AGE, date.today().month, date.today().day)
        end_date = date(date.today().year - UserBirthdate.MIN_AGE, date.today().month, date.today().day)
        delta = end_date - start_date
        if random.randint(0, 1) == 0:
            return start_date - timedelta(days=random.randint(1, delta.days))
        else:
            return end_date + timedelta(days=random.randint(1, delta.days))
    
    @classmethod
    def get_created_date(cls) -> date:
        return date(random.randint(2000, 2021), random.randint(1, 12), random.randint(1, 28))