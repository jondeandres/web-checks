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

    return parser.parse_args()



def _build_producer(args: argparse.Namespace) -> ConfluentProducer:
    return ConfluentProducer(KafkaConfig(brokers=args.kafka_brokers,
                                         ssl_key_path=args.kafka_ssl_key_path,
                                         ssl_certificate_path=args.kafka_ssl_cert_path,
                                         ssl_ca_path=args.kafka_ssl_ca_path))

