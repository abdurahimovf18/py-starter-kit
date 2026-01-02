

class ApplicationException(BaseException):
    def __init__(self, message: str, *args: object, **kwargs: object) -> None:
        self._message = message
        super().__init__(message, *args, **kwargs)
        
    @property
    def message(self) -> str:
        return self._message
    