import asyncio
import argparse
import logging

from checks.worker import Worker
from checks.repositories.hardcoded import HardCoded
from checks.writers.kafka import Kafka as KafkaWriter
from checks.lib.kafka.config import Config as KafkaConfig
from checks.lib.kafka.confluent_producer import ConfluentProducer
from checks.lib.serializers import ResultToJSON
from checks.jobs.http_check import HTTPCheck


_DEFAULT_LOGGING_FORMAT = '%(asctime)s %(name)s %(levelname)-8s %(message)s'
_LOGGING_OPTIONS = ['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL']


def bootstrap() -> None:
    args = _parse_args()

    logging.basicConfig(level=args.log_level,
                        format=_DEFAULT_LOGGING_FORMAT)

    _run_worker(args)


def _run_worker(args: argparse.Namespace):
    worker = Worker(HTTPCheck(),
                    HardCoded(),
                    KafkaWriter(_build_producer(args), args.kafka_topic, ResultToJSON()))

    asyncio.run(worker.run())


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kafka-brokers", required=True, nargs='+')
    parser.add_argument("--kafka-topic", required=True)
    parser.add_argument("--kafka-ssl-key-path")
    parser.add_argument("--kafka-ssl-cert-path")
    parser.add_argument("--kafka-ssl-ca-path")
    parser.add_argument("--log-level", choices=_LOGGING_OPTIONS, default='INFO')

    return parser.parse_args()



def _build_producer(args: argparse.Namespace) -> ConfluentProducer:
    return ConfluentProducer(KafkaConfig(brokers=args.kafka_brokers,
                                         ssl_key_path=args.kafka_ssl_key_path,
                                         ssl_certificate_path=args.kafka_ssl_cert_path,
                                         ssl_ca_path=args.kafka_ssl_ca_path))

