from abc import ABC, abstractmethod
import typing


class Job(ABC):
    """Represents a job to be executed by a Worker
    """
    @abstractmethod
    def run(self, objects: typing.Any) -> None:
        """
        Runs the logic using a collection of object as input

        Args:
          objects: any object
        """
        pass
