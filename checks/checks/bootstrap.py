import asyncio
import argparse

from checks.worker import Worker
from checks.repositories.hardcoded import HardCoded
from checks.writers.kafka import Kafka as KafkaWriter
from checks.lib.kafka.config import Config as KafkaConfig
from checks.lib.kafka.confluent_producer import ConfluentProducer
from checks.lib.serializers import ResultToJSON
from checks.jobs.http_check import HTTPCheck


def bootstrap() -> None:
    args = _parse_args()

    worker = Worker(HTTPCheck(),
                    HardCoded(),
                    KafkaWriter(_build_producer(args), args.topic, ResultToJSON()))

    asyncio.run(worker.run())


def _build_producer(args: argparse.Namespace) -> ConfluentProducer:
    return ConfluentProducer(KafkaConfig(brokers=args.brokers,
                                         ssl_key_path=args.ssl_key_path,
                                         ssl_certificate_path=args.ssl_cert_path,
                                         ssl_ca_path=args.ssl_ca_path))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brokers", required=True, nargs='+')
    parser.add_argument("--topic", required=True)
    parser.add_argument("--ssl-key-path")
    parser.add_argument("--ssl-cert-path")
    parser.add_argument("--ssl-ca-path")

    return parser.parse_args()
