from abc import ABC, abstractmethod
import typing


class Repository(ABC):
    """Abstracts the logic to fetch data to be used by a worker
    """
    @abstractmethod
    def get_objects(self) -> typing.List[typing.Any]:
        """
        Public interface of the repositories to get objects. Each children
        class will have specific logic based on the data to be returned or the
        source of data.

        Returns:
          A list of objects
        """
        pass
