from core_test.user.test_data import UserDataFactory as CoreUserDataFactory
from typing import Dict, Any, List
import random
from core_test.images_data import get_base64_string

class UserDataFactory(CoreUserDataFactory):
    @classmethod
    def generate_user_sign_up_user_request(cls) -> Dict[str, Any]:
        user = cls.generate_user_account()
        return {
            'phone_number': user.phone_number,
            'email': user.email,
            'name': user.name,
            'gender': user.gender.value,
            'password': user.password,
            'birthdate': user.birthdate.isoformat(),
        }
        
    @classmethod
    def generate_employee_sign_up_employee_request(cls, roles: List[str]) -> Dict[str, Any]:
        user = cls.generate_employee_account()
        return {
            'phone_number': user.phone_number,
            'email': user.email,
            'name': user.name,
            'gender': user.gender.value,
            'password': user.password,
            'birthdate': user.birthdate.isoformat(),
            'employee_data': {
                'dni': user.dni,
                'address': user.address,
                'photo': get_base64_string(),
                'roles': random.sample(roles, k=random.randint(1, len(roles))),
                'categories': [category.value for category in user.categories],
            }
        }

    @classmethod
    def generate_sign_in_request(cls) -> Dict[str, Any]:
        user = cls.generate_user_account()
        return {
            'phone_number': user.phone_number,
            'password': user.password,
        }
    
    @classmethod
    def generate_create_role_request(cls) -> Dict[str, Any]:
        role = cls.generate_role()
        return {
            'name': role.name,
            'accesses': [
                {
                    'access': access.access_type.value,
                    'permissions': [permission.value for permission in access.permissions],
                }
                for access in role.accesses
            ]
        }