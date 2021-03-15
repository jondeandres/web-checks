import datetime
import pytest

from writer.jobs.write_http_check_results import WriteHTTPCheckResults
from writer.model.http_check_result import HTTPCheckResult


class TestWriteHTTPCHeckResults:
    def test_run(self, db_conn):
        job = WriteHTTPCheckResults(db_conn)
        results = [
            HTTPCheckResult(url='https://aiven.io',
                            status_code=200,
                            response_time=123,
                            re_match=True,
                            error=None),
            HTTPCheckResult(url='https://github.com',
                            status_code=200,
                            response_time=321,
                            re_match=False,
                            error=None)
        ]

        job.run(results)

        with db_conn.cursor() as cur:
            cur.execute("""
                SELECT timestamp, url, status_code,response_time, re_match, error
                FROM http_check_result
                ORDER BY timestamp ASC
            """)

            rows = cur.fetchall()

            assert isinstance(rows[0][0], datetime.datetime) is True
            assert rows[0][1] == 'https://aiven.io'
            assert rows[0][2] == 200
            assert rows[0][3] == 123
            assert rows[0][4] is True
            assert rows[0][5] is None

            assert isinstance(rows[1][0], datetime.datetime) is True
            assert rows[1][1] == 'https://github.com'
            assert rows[1][2] == 200
            assert rows[1][3] == 321
            assert rows[1][4] is False
            assert rows[1][5] is None
