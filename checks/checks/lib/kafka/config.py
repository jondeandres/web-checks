from dataclasses import dataclass, field
import typing


_MAX_RETRIES = 3
_ACKS = 'all'


@dataclass
class Config:
    """
    Data class to store the Kafka configuration
    """

    brokers: typing.List[str]
    acks: typing.Optional[str] = field(default=_ACKS)
    retries: typing.Optional[int] = field(default=_MAX_RETRIES)
    ssl_key_path: typing.Optional[str] = None
    ssl_certificate_path: typing.Optional[str] = None
    ssl_ca_path: typing.Optional[str] = None
