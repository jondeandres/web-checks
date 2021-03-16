import logging
import typing

from confluent_kafka import Consumer as ConfluentConsumer


log = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 1


class Consumer:
    def __init__(self, topics: typing.List[str], options: typing.Dict[str, typing.Any]):
        config = {
            'bootstrap.servers': ','.join(options['brokers']),
            'group.id': options['group_id'],
            'client.id': 'confluent_client',
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest'
        }

        self.__topics = topics
        self.__consumer = ConfluentConsumer(config, logger=log)

    def subscribe(self):
        self.__consumer.subscribe(self.__topics)

    def consume(self, batch_size, timeout=_DEFAULT_TIMEOUT):
        return [
            message.value()
            for message in self.__consumer.consume(batch_size, timeout=timeout)
        ]

    def stop(self):
        self.__consumer.close()

    def commit(self) -> None:
        self.__consumer.commit()