import json
import pytest
import random
import threading
import time

import confluent_kafka

from writer.worker import Worker
from writer.deserializers.json_to_http_check_result import JSONToHTTPCheckResult
from writer.jobs.write_http_check_results import WriteHTTPCheckResults
from writer.lib.kafka.consumer import Consumer


def worker_thread(worker):
    worker.start()
    worker.run()


class TestWorker:
    def test_run(self, db_conn):
        # topic = 'checks-tests-%d' % random.randint(0, 100)
        topic = 'functional-tests'

        consumer = Consumer(
            [topic],
            {
                'brokers': ['test_kafka:29092'],
                'group_id': 'functional-tests'
            }
        )
        worker = Worker(
            consumer,
            WriteHTTPCheckResults(db_conn),
            JSONToHTTPCheckResult()
        )

        self._produce_messages(topic)

        app_thread = threading.Thread(target=worker_thread,
                                  args=(worker,),
                                  daemon=True)

        app_thread.start()

        time.sleep(5)

        with db_conn.cursor() as cur:
            cur.execute('SELECT * FROM http_check_result')

            rows = cur.fetchall()

            assert len(rows) == 2

        worker.stop()
        app_thread.join()

    def _produce_messages(self, topic):
        producer = confluent_kafka.Producer(
            {
                'bootstrap.servers': 'test_kafka:29092',
                'acks': 'all',
                'retries': 3
            }
        )

        messages = [
            {
                'url': 'https://aiven.io',
                'status_code': 200,
                'response_time': 123,
                're_match': False,
                'error': None
            },
            {
                'url': 'https://github.com.io',
                'status_code': 200,
                'response_time': 321,
                're_match': True,
                'error': None
            }
        ]

        for message in messages:
            producer.produce(topic, value=json.dumps(message))

        producer.flush(5)
