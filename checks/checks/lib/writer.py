from abc import ABC, abstractmethod
import typing

from checks.lib.result import Result


class Writer(ABC):
    """
    Writes the received list of Result into an external system. Each children
    class will take care of the specific details of the system and formats
    to be used.
    """
    @abstractmethod
    def write(self, results: typing.List[Result]) -> None:
        """
        Writes the received objects into a different system

        Args:
          objects: a list of Result objects
        """
        pass
