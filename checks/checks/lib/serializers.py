from abc import ABC, abstractmethod
from dataclasses import asdict
import json
import typing


from checks.lib.result import Result


class Serializer(ABC):
    """
    Abstract class to represent serializer objects.

    They have a single public method dump() that can be used to getLogger
    a string representation of that object.
    """
    @abstractmethod
    def dump(self, obj: typing.Any) -> str:
        pass


class ResultToJSON(Serializer):
    """
    Serializes a Result object to JSON
    """
    def dump(self, result: Result) -> str:
        """
        Dumps the received result to JSON

        Args:
          result: A Result object to be serialized

        Returns:
          A JSON string representing the received Result
        """
        return json.dumps(asdict(result))
