from dataclasses import dataclass
import typing


@dataclass
class Config:
    """
    Data class to store the Kafka configuration
    """

    brokers: typing.List[str]
    group_id: str
    topics: typing.List[str]
    ssl_key_path: typing.Optional[str] = None
    ssl_certificate_path: typing.Optional[str] = None
    ssl_ca_path: typing.Optional[str] = None
