from abc import ABC, abstractmethod
import typing


class Serializer(ABC):
    """
    Abstract class to represent serializer objects.

    They have a single public method dump() that can be used to getLogger
    a string representation of that object.
    """
    @abstractmethod
    def dump(self, obj: typing.Any) -> str:
        pass
