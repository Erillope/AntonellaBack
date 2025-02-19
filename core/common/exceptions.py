class SystemException(Exception): ...

class InvalidOrderDirectionException(SystemException):
    @classmethod
    def invalid_direction(cls, direction: str) -> "InvalidOrderDirectionException":
        return cls(f"'{direction}'no es una dirección válida.")

class InvalidIdException(SystemException):
    @classmethod
    def invalid_id(cls, id: str) -> "InvalidIdException":
        return cls(f"El id '{id}' es inválido")


class InvalidBase64FormatException(SystemException):
    @classmethod
    def invalid_format(cls) -> 'InvalidBase64FormatException':
        return cls("El formato que ha ingresado no es un formato base64 válido.")


class MediaNotFoundException(SystemException):
    @classmethod
    def media_not_found(cls, media: str) -> "MediaNotFoundException":
        return cls(f"la media {media} no fue encontrada")