from dataclasses import dataclass
import typing


@dataclass
class Target:
    url: str
    regex: typing.Optional[str] = None
