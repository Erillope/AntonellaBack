import json
from typing import List, Dict, Any, Optional, Tuple
from core.common import ID
from core.user import AccountStatus, Gender, UserAccount, UserAccountFactory, RoleFactory, Role
from core.user.domain.values import UserBirthdate
from core.user.service.dto import SignUpDto
import random
from datetime import date, timedelta

class UserTestData:
    instance: Optional['UserTestData'] = None
    
    def __init__(self) -> None:
        self.data: Dict[str, List[Any]] = {}
        with open('project_test/user/user_test_data.json') as file:
            self.data = json.load(file)
    
    @classmethod
    def get_instance(cls) -> 'UserTestData':
        if cls.instance is None:
            cls.instance = UserTestData()
        return cls.instance
    
    def get_user_names(self) -> List[str]:
        return self.data['user_names']
    
    def get_invalid_user_names(self) -> List[str]:
        return self.data['invalid_user_names']
    
    def get_emails(self) -> List[str]:
        return self.data['emails']
    
    def get_invalid_emails(self) -> List[str]:
        return self.data['invalid_emails']
    
    def get_passwords(self) -> List[str]:
        return self.data['passwords']

    def get_invalid_passwords(self) -> List[str]:
        return self.data['invalid_passwords']
    
    def get_phone_numbers(self) -> List[str]:
        return self.data['phone_numbers']
    
    def get_invalid_phone_numbers(self) -> List[str]:
        return self.data['invalid_phone_numbers']
    
    def get_roles(self) -> List[str]:
        return self.data['roles']
    
    def get_sample_list_roles(self) -> List[str]:
        return random.sample(self.get_roles(), random.randint(1, len(self.get_roles())))
    
    def get_invalid_roles(self) -> List[str]:
        return self.data['invalid_roles']
    
    def get_invalid_ids(self) -> List[str]:
        return self.data['invalid_ids']
    
    def get_account_status(self) -> AccountStatus:
        return random.choice(list(AccountStatus))
    
    def get_gender(self) -> Gender:
        return random.choice(list(Gender))
    
    def get_birthdate(self) -> date:
        start_date = date(date.today().year - UserBirthdate.MAX_AGE, date.today().month, date.today().day)
        end_date = date(date.today().year - UserBirthdate.MIN_AGE, date.today().month, date.today().day)
        delta = end_date - start_date
        return start_date + timedelta(days=random.randint(0, delta.days))
    
    def get_invalid_birthdate(self) -> date:
        start_date = date(date.today().year - UserBirthdate.MAX_AGE, date.today().month, date.today().day)
        end_date = date(date.today().year - UserBirthdate.MIN_AGE, date.today().month, date.today().day)
        delta = end_date - start_date
        if random.randint(0, 1) == 0:
            return start_date - timedelta(days=random.randint(1, delta.days))
        else:
            return end_date + timedelta(days=random.randint(1, delta.days))
    
    def get_created_date(self) -> date:
        return date(random.randint(2000, 2021), random.randint(1, 12), random.randint(1, 28))

class DataFactory:
    user_test_data: UserTestData = UserTestData.get_instance()
    @classmethod
    def generate_sign_up_dtos(cls) -> List[SignUpDto]:
        return [SignUpDto(
            name=cls.user_test_data.get_user_names()[i],
            email=cls.user_test_data.get_emails()[i],
            password=cls.user_test_data.get_passwords()[i],
            phone_number=cls.user_test_data.get_phone_numbers()[i],
            birthdate=cls.user_test_data.get_birthdate(),
            roles=cls.user_test_data.get_sample_list_roles(),
            gender=cls.user_test_data.get_gender()
        ) for i in range(10)]
    
    @classmethod
    def generate_user_accounts(cls) -> List[UserAccount]:
        return [UserAccountFactory.load(
            id=ID.generate(),
            name=cls.user_test_data.get_user_names()[i],
            email=cls.user_test_data.get_emails()[i],
            password=cls.user_test_data.get_passwords()[i],
            phone_number=cls.user_test_data.get_phone_numbers()[i],
            birthdate=cls.user_test_data.get_birthdate(),
            status=cls.user_test_data.get_account_status(),
            gender=cls.user_test_data.get_gender(),
            created_date=cls.user_test_data.get_created_date(),
            roles=cls.generate_sample_roles()
        ) for i in range(10)]
    
    @classmethod
    def generate_sample_roles(cls) -> List[Role]:
        return [RoleFactory.load(
            id=ID.generate(),
            name=role_name,
            created_date=cls.user_test_data.get_created_date(),
        ) for role_name in cls.user_test_data.get_sample_list_roles()]
    
    @classmethod
    def generate_roles(cls) -> List[Role]:
        return [RoleFactory.load(
            id=ID.generate(),
            name=role_name,
            created_date=cls.user_test_data.get_created_date(),
        ) for role_name in cls.user_test_data.get_roles()]
    
    @classmethod
    def generate_user_with_info(cls) -> List[Tuple[UserAccount, str, str]]:
        info = []
        for i in range(10):
            phone_number = cls.user_test_data.get_phone_numbers()[i]
            password = cls.user_test_data.get_passwords()[i]
            user = UserAccountFactory.load(
                    id=ID.generate(),
                    name=cls.user_test_data.get_user_names()[i],
                    email=cls.user_test_data.get_emails()[i],
                    password=password,
                    phone_number=phone_number,
                    birthdate=cls.user_test_data.get_birthdate(),
                    status=cls.user_test_data.get_account_status(),
                    gender=cls.user_test_data.get_gender(),
                    created_date=cls.user_test_data.get_created_date(),
                    roles=cls.generate_sample_roles()
                )
            info.append((user, phone_number, password))
        return info