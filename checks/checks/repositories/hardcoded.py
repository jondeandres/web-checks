import typing

from checks.lib.repository import Repository
from checks.model.target import Target


class HardCoded(Repository):
    def get_objects(self) -> typing.List[Target]:
        return [
            Target(url='https://github.com'),
            Target(url='https://aiven.io/')
        ]
