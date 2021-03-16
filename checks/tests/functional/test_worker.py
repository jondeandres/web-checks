import asyncio
import json
import logging
import random
import time
import threading

from confluent_kafka import Consumer

from checks.worker import Worker
from checks.lib.repository import Repository
from checks.model.target import Target
from checks.writers.kafka import Kafka as KafkaWriter
from checks.lib.kafka.config import Config as KafkaConfig
from checks.lib.kafka.confluent_producer import ConfluentProducer
from checks.lib.serializers import ResultToJSON
from checks.jobs.http_check import HTTPCheck


brokers = ['test_kafka:29092']
log = logging.getLogger(__name__)


class DummyRepository(Repository):
    def get_objects(self):
        return [Target(url='https://aiven.io', regex='.*mirrormaker.*')]


def worker_thread(worker):
    asyncio.run(worker.run())


class TestWorker:
    def test_run(self):
        topic = 'checks-tests-%d' % random.randint(0, 100)
        worker = Worker(HTTPCheck(),
                        DummyRepository(),
                        KafkaWriter(ConfluentProducer(KafkaConfig(brokers=brokers)), topic, ResultToJSON()),
                        period=1)
        app_thread = threading.Thread(target=worker_thread,
                                  args=(worker,),
                                  daemon=True)

        app_thread.start()
        time.sleep(2)

        worker.stop()
        app_thread.join()

        consumer = Consumer({
            'bootstrap.servers': '.'.join(brokers),
            'group.id': 'functional-tests',
            'client.id': 'confluent_client',
            'enable.auto.commit': True,
            'auto.offset.reset': 'earliest'
        }, logger=log)

        consumer.subscribe([topic])

        message = json.loads(consumer.consume(1, timeout=5)[0].value())

        assert message['url'] == 'https://aiven.io'
        assert type(message['status_code']) == int
        assert message['re_match'] is True
        assert type(message['response_time']) == int
