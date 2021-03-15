import logging
import typing

import confluent_kafka
from confluent_kafka import KafkaError

from checks.lib.kafka.producer import Producer
from checks.lib.kafka.config import Config


log = logging.getLogger(__name__)

_FLUSH_TIMEOUT = 3


class ConfluentProducer(Producer):
    """
    Kafka producer using confluent_kafka library
    """
    def __init__(self, config: Config):
        self.__config = config
        self.__producer = confluent_kafka.Producer(self.__build_config(config), logger=log)

    def produce(self, topic: str, value: str) -> None:
        """
        Produces a Kafka message

        Args:
          topic: A string representing the topic to produce to
          value: A string wih the value to send to the network
        """

        self.__producer.produce(topic=topic, value=value)

    def flush(self, timeout: int = _FLUSH_TIMEOUT) -> None:
        """
        Waits for all the messages in the internal producer queue to be sent.

        This is a blocking call.

        Args:
          timeout: An integer representing the maximum time to wait for
            the queue to drain
        """
        self.__producer.flush(timeout)

    def __build_config(self, config: Config) -> typing.Dict[str, typing.Any]:
        options = {
            'bootstrap.servers': ','.join(config.brokers),
            'acks': config.acks,
            'retries': config.retries,
            'error_cb': self.__error_cb
        }

        if config.ssl_key_path:
            options['security.protocol'] = 'ssl'
            options['ssl.key.location'] = config.ssl_key_path

        if config.ssl_certificate_path:
            options['ssl.certificate.location'] = config.ssl_certificate_path

        if config.ssl_ca_path:
            options['ssl.ca.location'] = config.ssl_ca_path

        return options

    @staticmethod
    def __error_cb(error: KafkaError) -> None:
        log.error('Kafka error: %s', error)
