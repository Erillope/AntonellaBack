from core_test.user.test_data import UserDataFactory as CoreUserDataFactory
from typing import Dict, Any, List
import random

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
                'photo': user.photo,
                'roles': random.sample(roles, k=random.randint(1, len(roles)))
            }
        }

    @classmethod
    def generate_sign_in_request(cls) -> Dict[str, Any]:
        user = cls.generate_user_account()
        return {
            'phone_number': user.phone_number,
            'password': user.password,
        }