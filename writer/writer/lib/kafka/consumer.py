import logging
import typing

from confluent_kafka import Consumer as ConfluentConsumer

from writer.lib.kafka.config import Config


log = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 1


class Consumer:
    def __init__(self, config: Config):
        self.__topics = config.topics
        self.__consumer = ConfluentConsumer(self._build_config(config), logger=log)

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

    def _build_config(self, config: Config):
        options = {
            'bootstrap.servers': ','.join(config.brokers),
            'group.id': config.group_id,
            'client.id': 'confluent_client',
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest'
        }

        if config.ssl_key_path:
            options['security.protocol'] = 'ssl'
            options['ssl.key.location'] = config.ssl_key_path

        if config.ssl_certificate_path:
            options['ssl.certificate.location'] = config.ssl_certificate_path

        if config.ssl_ca_path:
            options['ssl.ca.location'] = config.ssl_ca_path

        return options
