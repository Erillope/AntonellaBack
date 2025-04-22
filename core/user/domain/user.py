from pydantic import BaseModel, model_validator, PrivateAttr
from datetime import date
from typing import Optional, List, ClassVar
from core.common import ID, Event
from core.common.image_storage import Base64ImageStorage, ImageSaved, ImageDeleted
from .values import *
from .events import UserAccountSaved

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
    _events: List[Event] = PrivateAttr(default=[])
    
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
                    status: Optional[AccountStatus]=None, birthdate: Optional[date]=None,
                    gender: Optional[Gender]=None) -> None:
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
        
        if birthdate is not None:
            self.birthdate = birthdate

        if gender is not None:
            self.gender = gender
            
        self._validate_data()
    
    def verify_password(self, password: str) -> bool:
        '''Verifica la contraseña de la cuenta de usuario'''
        return UserPassword.verify(self.password, password)
    
    def verify_account(self, phone_number: str, password: str) -> bool:
        '''Verifica la cuenta de usuario'''
        return self.phone_number == phone_number and self.verify_password(password)
    
    def save(self, update: bool=False) -> None:
        UserAccountSaved(user=self, update=update).publish()
        for event in self._events:
            event.publish()
        self._events.clear()


class EmployeeAccount(UserAccount):
    dni: str
    address: str
    roles: List[str]
    photo: str
    categories: List[EmployeeCategories]
    IMAGE_PATH: ClassVar[str] = f'employee'
    
    def _validate_data(self) -> None:
        super()._validate_data()
        self.set_photo(self.photo)
        DniValue.validate(self.dni)
    
    def change_data(self, phone_number: Optional[str]=None, email: Optional[str]=None,
                    name: Optional[str]=None, password: Optional[str]=None,
                    status: Optional[AccountStatus]=None, birthdate: Optional[date]=None,
                    gender: Optional[Gender]=None, address: Optional[str]=None, dni: Optional[str]=None,
                    photo: Optional[str]=None, roles: Optional[List[str]]=None,
                    categories: Optional[List[EmployeeCategories]] = None) -> None:
        super().change_data(phone_number, email, name, password, status, birthdate, gender)
        if dni is not None:
            self.dni = dni
        if address is not None:
            self.address = address
        if photo is not None:
            if (photo != self.photo):
                self._events.append(ImageDeleted(image_urls=[self.photo]))
            self.photo = photo
        if roles is not None:
            self.roles = roles
        if categories is not None:
            self.categories = categories
        self._validate_data()

    def set_photo(self, photo: str) -> None:
        '''Establece la foto de perfil de la cuenta de usuario'''
        if Base64ImageStorage.is_media_url(photo):
            self.photo = photo
            return
        image = Base64ImageStorage(folder=self.IMAGE_PATH, base64_image=photo)
        self.photo = image.get_url()
        self._events.append(ImageSaved(images=[image]))
        
        
class UserAccountFactory:
    @staticmethod
    def create_user(phone_number: str, email: str, name: str, password: str, birthdate: date, gender: Gender) -> UserAccount:
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
        )
    
    @staticmethod
    def load_user(id: str, phone_number: str, email: str, name: str, password: str, status: AccountStatus, 
             birthdate: date, created_date: date, gender: Gender) -> UserAccount:
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
        )
    
    @staticmethod
    def create_employee(phone_number: str, email: str, name: str, password: str, birthdate: date,
                        gender: Gender, dni: str, address: str, photo: str, roles: List[str],
                        categories: List[EmployeeCategories]) -> EmployeeAccount:
        return EmployeeAccount(
            id = ID.generate(),
            phone_number = phone_number,
            email = email,
            name = name,
            password = password,
            status = AccountStatus.ENABLE,
            birthdate= birthdate,
            created_date = date.today(),
            gender=gender,
            dni=dni,
            address=address,
            photo=photo,
            roles=roles,
            categories=categories
        )
    
    @staticmethod
    def load_employee(id: str, phone_number: str, email: str, name: str, password: str,
                      status: AccountStatus, birthdate: date, created_date: date, gender: Gender,
                      dni: str, address: str, photo: str, roles: List[str],
                      categories: List[EmployeeCategories]) -> EmployeeAccount:
        return EmployeeAccount(
            id = id,
            phone_number = phone_number,
            email = email,
            name = name,
            password = password,
            status = status,
            birthdate= birthdate,
            created_date = created_date,
            gender=gender,
            dni=dni,
            address=address,
            roles=roles,
            photo=photo,
            categories=categories
        )