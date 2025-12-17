from src.core.base.exceptions.base_application_exception import BaseApplicationException


class ContainerException(BaseApplicationException):
    pass


class InterfaceNotRegisteredError(ContainerException):
    """
    Raised on attempt to access unregistered Interface.
    """
    pass


class InterfaceAlreadyRegisteredError(ContainerException):
    """
    Raised on attempt to register the realization of the same interface twice.
    """
    pass
