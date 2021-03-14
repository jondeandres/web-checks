from abc import ABC, abstractmethod


class Producer(ABC):
    @abstractmethod
    def produce(self, topic: str, value: str) -> None:
        pass
