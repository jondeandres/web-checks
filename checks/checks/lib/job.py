from abc import ABC, abstractmethod
import typing

from checks.lib.result import Result


class Job(ABC):
    """Represents a job to be executed by a Worker
    """
    @abstractmethod
    def run(self, obj: typing.Any) -> Result:
        """
        Runs the logic using a single object as input

        Args:
          obj: any object

        Returns:
          A Result object
        """
        pass
