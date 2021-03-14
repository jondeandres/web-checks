import typing

from checks.lib.writer import Writer
from checks.lib.result import Result
from checks.lib.kafka.producer import Producer
from checks.lib.serializers import Serializer


class Kafka(Writer):
    """
    A Writer implementation that uses a Kafka Producer and a Serializer
    """
    def __init__(self, producer: Producer, topic: str, serializer: Serializer):
        self.__producer = producer
        self.__topic = topic
        self.__serializer = serializer

    def write(self, results: typing.List[Result]):
        """
        Produces messages to Kafka using the received Result objects.

        It'll serialize each Result using the Serialier and will wait
        for the internal queue to be empty

        Args:
          results: A list of Result objects
        """
        for res in results:
            self.__producer.produce(self.__topic,
                                    self.__serializer.dump(res))

        # Wait for all messages to be sent
        self.__producer.flush()
