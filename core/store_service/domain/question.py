from pydantic import BaseModel, model_validator, PrivateAttr
from core.common import ID, Event
from .events import QuestionSaved, QuestionDeleted, ChoiceAdded, ChoiceDeleted, ChoiceImageAdded, ChoiceImageDeleted
from .values import InputType, Choice
from .exceptions import MissingStoreServiceException, OptionAlreadyExistsException
from typing import List, Optional, ClassVar
from datetime import date
from core.common.image_storage import Base64ImageStorage

class Question(BaseModel):
    id: str
    title: str
    created_date: date
    _store_service_id: str = PrivateAttr(default='')
    _events: List[Event] = PrivateAttr(default=[])
    
    @model_validator(mode='after')
    def validate_data(self) -> 'Question':
        '''Valida los datos de la pregunta de formulario'''
        self._validate_data()
        return self
    
    def _validate_data(self) -> None:
        ID.validate(self.id)
        self.title = self.title.lower()
    
    def set_store_service(self, store_service_id: str) -> None:
        '''Establece el servicio de tienda al que pertenece la pregunta'''
        self._store_service_id = store_service_id
    
    def get_store_service(self) -> str:
        '''Obtiene el servicio de tienda al que pertenece la pregunta'''
        return self._store_service_id
        
    def change_data(self, title: Optional[str]=None) -> None:
        '''Cambia los datos de la pregunta de formulario'''
        if title is not None:
            self.title = title
        
        self._validate_data()
    
    def save(self) -> None:
        '''Guarda la pregunta de formulario'''
        if self._store_service_id:
            QuestionSaved(question=self).publish()
            for event in self._events:
                event.publish()
            return
        raise MissingStoreServiceException.not_asigned()

    def delete(self) -> None:
        '''Elimina la pregunta de formulario'''
        QuestionDeleted(question=self).publish()
        

class FormQuestion(Question):
    input_type: InputType
    

class TextChoiceQuestion(Question):
    choices: List[str] = []
    
    def add_choice(self, option: str) -> None:
        '''Agrega una opción a la pregunta de selección'''
        if option in self.choices: raise OptionAlreadyExistsException.already_exists(option)
        self.choices.append(option)
        self._events.append(ChoiceAdded(question_id=self.id, option=option))
    
    def remove_choice(self, option: str) -> None:
        '''Elimina una opción de la pregunta de selección'''
        if option not in self.choices: return
        self.choices.remove(option)
        self._events.append(ChoiceDeleted(question_id=self.id, option=option))


class ImageChoiceQuestion(Question):
    choices: List[Choice] = []
    IMAGE_PATH: ClassVar[str] = f'choices'
    
    def add_choice(self, option: str, base64_image: str) -> None:
        '''Agrega una opción a la pregunta de selección'''
        image = Base64ImageStorage(folder=self.IMAGE_PATH, base64_image=base64_image)
        choice = Choice(option=option, image_url=image.get_url())
        if choice in self.choices: raise OptionAlreadyExistsException.already_exists(option)
        self.choices.append(choice)
        self._events.append(ChoiceImageAdded(question_id=self.id, option=choice.option, image=image))
    
    def remove_choice(self, option: str) -> None:
        '''Elimina una opción de la pregunta de selección'''
        for choice in self.choices:
            if choice.option == option:
                self.choices.remove(choice)
                self._events.append(ChoiceImageDeleted(question_id=self.id,
                                                       option=choice.option, image_url=choice.image_url))


class QuestionFactory:
    @staticmethod
    def create_form_question(title: str, input_type: InputType) -> FormQuestion:
        return FormQuestion(
            id=ID.generate(),
            title = title,
            input_type = input_type,
            created_date = date.today()
        )
    
    @staticmethod
    def create_text_choice_question(title: str) -> TextChoiceQuestion:
        return TextChoiceQuestion(
            id = ID.generate(),
            title = title,
            created_date = date.today()
        )
    
    @staticmethod
    def create_image_choice_question(title: str) -> ImageChoiceQuestion:
        return ImageChoiceQuestion(
            id = ID.generate(),
            title = title,
            created_date = date.today()
        )
    
    @staticmethod
    def load_form_question(id: str, title: str, input_type: InputType,
                           created_date: date, store_service_id: str) -> FormQuestion:
        form_question = FormQuestion(
            id = id,
            title = title,
            input_type = input_type,
            created_date = created_date
        )
        form_question.set_store_service(store_service_id)
        return form_question
    
    @staticmethod
    def load_text_choice_question(id: str, title: str, choices: List[str],
                                  created_date: date, store_service_id: str) -> TextChoiceQuestion:
        text_choice_question = TextChoiceQuestion(
            id = id,
            title = title,
            choices = choices,
            created_date = created_date
        )
        text_choice_question.set_store_service(store_service_id)
        return text_choice_question
    
    @staticmethod
    def load_image_choice_question(id: str, title: str, choices: List[Choice],
                                   created_date: date, store_service_id: str) -> ImageChoiceQuestion:
        image_choice_question = ImageChoiceQuestion(
            id = id,
            title = title,
            choices = choices,
            created_date = created_date
        )
        image_choice_question.set_store_service(store_service_id)
        return image_choice_question