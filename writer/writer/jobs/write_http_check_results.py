import logging
import typing

import psycopg2
import psycopg2.extras


from writer.lib.job import Job
from writer.model.http_check_result import HTTPCheckResult


_INSERT_TMPL = """
    INSERT INTO http_check_result
    (url, status_code, response_time, re_match, error)
    VALUES %s
"""


log = logging.getLogger(__name__)


class WriteHTTPCheckResults(Job):
    """
    Persists HTTPCheckResult collections to DB
    """
    def __init__(self, conn):
        self.__conn = conn

    def run(self, results: typing.List[HTTPCheckResult]):
        data = [
            (res.url, res.status_code, res.response_time, res.re_match, res.error)
            for res in results
        ]
        try:
            with self.__conn.cursor() as cur:
                psycopg2.extras.execute_values (
                    cur, _INSERT_TMPL, data
                )
        except Exception:
            log.error('Error writing to DB', exc_info=True)

            raise
