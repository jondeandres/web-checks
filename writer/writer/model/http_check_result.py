from dataclasses import dataclass
import typing

from writer.lib.result import Result


@dataclass
class HTTPCheckResult(Result):
    """
    Represents the result consumed from a Kafka message
    """
    url: str
    response_time: int
    status_code: typing.Optional[int] = None
    re_match: typing.Optional[bool] = None
    error: typing.Optional[str] = None
