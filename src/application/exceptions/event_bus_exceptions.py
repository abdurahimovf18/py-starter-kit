from src.shared.exceptions import ApplicationException, SetupError


class EventBusException(ApplicationException):
    pass


class EventBusAlreadyStartedError(EventBusException, SetupError):
    """
    Raised on attempt to call .start method second time without closing.
    """
    pass


class EventBusAlreadyClosedError(EventBusException, SetupError):
    """
    Raised on attempt to call .close method second time without starting.
    """
    pass


class EventBusNotStartedError(EventBusException, SetupError):
    """
    Raised on attempt to use event bus before starting it.
    """
    pass
