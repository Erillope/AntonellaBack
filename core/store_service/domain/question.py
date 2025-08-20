from pydantic import BaseModel, model_validator, PrivateAttr
from core.common import ID, Event
from .events import QuestionSaved, QuestionDeleted
from .values import InputType, Choice
from .exceptions import MissingStoreServiceException
from typing import List, Optional, ClassVar
from datetime import date
from core.common.image_storage import Base64ImageStorage, ImageSaved, ImageDeleted

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
    choices: List[str]
    
    def change_data(self, title: Optional[str]=None, choices: Optional[List[str]]=None) -> None:
        super().change_data(title)
        if choices is not None:
            self.choices = choices


class ImageChoiceQuestion(Question):
    choices: List[Choice]
    IMAGE_PATH: ClassVar[str] = f'choices'
    
    def _validate_data(self) -> None:
        super()._validate_data()
        self.set_choices(self.choices)
    
    def change_data(self, title: Optional[str]=None, choices: Optional[List[Choice]]=None) -> None:
        super().change_data(title)
        if choices is not None:
            images = [choice.image for choice in choices]
            self._events.append(ImageDeleted(image_urls=[choice.image for choice in self.choices if choice.image not in images]))
            self.choices = choices
        self._validate_data()

    def set_choices(self, choices: List[Choice]) -> None:
        self.choices = []
        for choice in choices:
            if Base64ImageStorage.is_media_url(choice.image):
                self.choices.append(choice)
            else:
                img = Base64ImageStorage(folder=self.IMAGE_PATH, base64_image=choice.image)
                self.choices.append(Choice(option=choice.option, image=img.get_url()))
                self._events.append(ImageSaved(images=[img]))

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
    def create_text_choice_question(title: str, choices: List[str]) -> TextChoiceQuestion:
        return TextChoiceQuestion(
            id = ID.generate(),
            title = title,
            choices = choices,
            created_date = date.today()
        )
    
    @staticmethod
    def create_image_choice_question(title: str, choices: List[Choice]) -> ImageChoiceQuestion:
        return ImageChoiceQuestion(
            id = ID.generate(),
            title = title,
            choices = choices,
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