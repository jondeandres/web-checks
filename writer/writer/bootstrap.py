import argparse
import logging

import psycopg2

from writer import db
from writer.worker import Worker
from writer.deserializers.json_to_http_check_result import JSONToHTTPCheckResult
from writer.jobs.write_http_check_results import WriteHTTPCheckResults
from writer.lib.kafka.consumer import Consumer
from writer.lib.kafka.config import Config as ConsumerConfig


_DEFAULT_LOGGING_FORMAT = '%(asctime)s %(name)s %(levelname)-8s %(message)s'
_LOGGING_OPTIONS = ['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL']


def bootstrap() -> None:
    args = _parse_args()

    logging.basicConfig(level=args.log_level,
                        format=_DEFAULT_LOGGING_FORMAT)

    conn = db.connect(database=args.db_name,
                      user=args.db_user,
                      password=args.db_password,
                      host=args.db_host,
                      port=args.db_port,
                      sslmode=args.db_sslmode,
                      sslrootcert=args.db_sslrootcert)
    db.prepare_db(conn)

    _run_worker(args, conn)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--db-name", required=True)
    parser.add_argument("--db-user", required=True)
    parser.add_argument("--db-password", required=True)
    parser.add_argument("--db-host", required=True)
    parser.add_argument("--db-port", default='5432')
    parser.add_argument("--db-sslmode", required=False)
    parser.add_argument("--db-sslrootcert", required=False)
    parser.add_argument("--kafka-brokers", required=False, nargs='+')
    parser.add_argument("--kafka-topics", required=True, nargs='+')
    parser.add_argument("--kafka-group-id", required=True)
    parser.add_argument("--kafka-ssl-key-path")
    parser.add_argument("--kafka-ssl-cert-path")
    parser.add_argument("--kafka-ssl-ca-path")
    parser.add_argument("--log-level", choices=_LOGGING_OPTIONS, default='INFO')

    return parser.parse_args()


def _run_worker(args: argparse.Namespace, conn: psycopg2.extensions.connection) -> None:
    consumer = Consumer(
        ConsumerConfig(
            brokers=args.kafka_brokers,
            topics=args.kafka_topics,
            group_id=args.kafka_group_id,
            ssl_key_path=args.kafka_ssl_key_path,
            ssl_certificate_path=args.kafka_ssl_cert_path,
            ssl_ca_path=args.kafka_ssl_ca_path
        )
    )
    worker = Worker(
        consumer,
        WriteHTTPCheckResults(conn),
        JSONToHTTPCheckResult()
    )

    worker.start()
    worker.run()
