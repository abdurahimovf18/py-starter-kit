from src.core.base.exceptions.base_application_exception import BaseApplicationException


class ApplicationException(BaseApplicationException):
    def __init__(self, message: str, *args: object, **kwargs: object) -> None:
        super().__init__(message, *args, **kwargs)
        