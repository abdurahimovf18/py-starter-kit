from src.shared.exceptions import ApplicationException, SetupError


class ContainerException(ApplicationException):
    pass


class InterfaceNotRegisteredError(ContainerException, SetupError):
    """
    Raised on attempt to access unregistered Interface.
    """
    pass


class InterfaceAlreadyRegisteredError(ContainerException, SetupError):
    """
    Raised on attempt to register the realization of the same interface twice.
    """
    pass
