from core.store_service.domain.exceptions import StoreServiceException

class MissingImageException(StoreServiceException):
    '''Excepción para cuando una imagen es requerida'''
    @classmethod
    def missing_image(cls) -> 'MissingImageException':
        return cls('Una imagen es requerida')


class QuestionAlreadyExistsException(StoreServiceException):
    '''Excepción para cuando una pregunta ya existe'''
    @classmethod
    def already_exists(cls, title: str) -> 'QuestionAlreadyExistsException':
        return cls(f'La pregunta "{title}" ya existe')