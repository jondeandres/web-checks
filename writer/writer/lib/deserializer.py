from abc import ABC, abstractmethod
import typing


class Deserializer(ABC):
    """
    Abstract class that defines the public interface
    to deserialize data objects
    """
    @abstractmethod
    def loads(self, obj: typing.Any) -> typing.Any:
        pass
