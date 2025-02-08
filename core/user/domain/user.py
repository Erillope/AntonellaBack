from pydantic import BaseModel, model_validator
from datetime import date
from typing import Optional, List
from core.common import ID, EventPublisher, Event
from .values import AccountStatus, Gender, UserPhoneNumber, UserEmail, UserName, UserPassword, UserBirthdate
from .role import Role
from .events import UserAccountSaved, RoleAddedToUser, RoleRemovedFromUser

class UserAccount(BaseModel):
    '''Cuenta de usuario'''
    id: str
    phone_number: str
    email: str
    name: str
    password: str
    status: AccountStatus
    gender: Gender
    birthdate: date
    created_date: date
    roles: List[Role]
    events: List[Event] = []
    
    @model_validator(mode='after')
    def validate_data(self) -> 'UserAccount':
        '''Valida los datos de la cuenta de usuario'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        self.email = self.email.lower()
        self.name = self.name.lower()
        ID.validate(self.id)
        UserPhoneNumber.validate(self.phone_number)
        UserEmail.validate(self.email)
        UserName.validate(self.name)
        UserPassword.validate(self.password)
        self.password = UserPassword.encode(self.password)
        UserBirthdate.validate(self.birthdate)
        
    def change_data(self, phone_number: Optional[str]=None, email: Optional[str]=None,
                    name: Optional[str]=None, password: Optional[str]=None,
                    status: Optional[AccountStatus]=None) -> None:
        '''Cambia los datos de la cuenta de usuario'''
        if phone_number is not None:
            self.phone_number = phone_number

        if email is not None:
            self.email = email

        if name is not None:
            self.name = name

        if password is not None:
            self.password = password

        if status is not None:
            self.status = status
        
        self._validate_data()
    
    def add_role(self, role: Role) -> None:
        '''Añade un rol a la cuenta de usuario'''
        self.roles.append(role)
        self.events.append(RoleAddedToUser(rolename=role.name, user_id=self.id))
    
    def remove_role(self, role: Role) -> None:
        '''Remueve un rol de la cuenta de usuario'''
        self.roles.remove(role)
        self.events.append(RoleRemovedFromUser(rolename=role.name, user_id=self.id))
        pass
    
    def verify_password(self, password: str) -> bool:
        '''Verifica la contraseña de la cuenta de usuario'''
        return UserPassword.verify(self.password, password)
    
    def verify_account(self, phone_number: str, password: str) -> bool:
        '''Verifica la cuenta de usuario'''
        return self.phone_number == phone_number and self.verify_password(password)
    
    def save(self) -> None:
        EventPublisher.publish(UserAccountSaved(user=self))
        for event in self.events:
            EventPublisher.publish(event)
        self.events.clear()


class UserAccountFactory:
    @staticmethod
    def create(phone_number: str, email: str, name: str, password: str, birthdate: date, gender: Gender) -> UserAccount:
        return UserAccount(
            id = ID.generate(),
            phone_number = phone_number,
            email = email,
            name = name,
            password = password,
            status = AccountStatus.ENABLE,
            birthdate= birthdate,
            created_date = date.today(),
            gender=gender,
            roles=[]
        )
    
    @staticmethod
    def load(id: str, phone_number: str, email: str, name: str, password: str, status: AccountStatus, 
             birthdate: date, created_date: date, gender: Gender, roles: List[Role]) -> UserAccount:
        '''Carga una cuenta de usuario existente'''
        return UserAccount(
            id = id,
            phone_number = phone_number,
            email = email,
            name = name,
            password = password,
            status = status,
            birthdate= birthdate,
            created_date = created_date,
            gender=gender,
            roles=roles
        )