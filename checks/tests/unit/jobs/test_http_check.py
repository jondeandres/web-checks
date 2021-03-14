import asyncio
from aioresponses import aioresponses
from aiohttp.client_exceptions import ClientError
import mock
import pytest

from checks.jobs.http_check import HTTPCheck
from checks.model.target import Target
from checks.model.http_check_result import HTTPCheckResult


class TestHTTPCheck:
    def setup_method(self):
        self.job = HTTPCheck()

    def test_run(self, event_loop):
        target = Target(url='https://foo.com')

        with mock.patch('time.time') as time:
            time.side_effect = [1000, 1000.1234]

            with aioresponses() as http:
                http.get('https://foo.com', status=200)

                result = event_loop.run_until_complete(self.job.run(target))

                assert result == HTTPCheckResult(url='https://foo.com',
                                                 status_code=200,
                                                 response_time=123,
                                                 re_match=None,
                                                 error=None)

    def test_run_on_success_re_match(self, event_loop):
        target = Target(url='https://foo.com', regex='.*bar.*')

        with mock.patch('time.time') as time:
            time.side_effect = [1000, 1001]

            with aioresponses() as http:
                http.get('https://foo.com', status=200, body='we can find bar here')

                result = event_loop.run_until_complete(self.job.run(target))

                assert result == HTTPCheckResult(url='https://foo.com',
                                                 status_code=200,
                                                 response_time=1000,
                                                 re_match=True,
                                                 error=None)

    def test_run_on_fail_re_match(self, event_loop):
        target = Target(url='https://foo.com', regex='.*bar.*')

        with mock.patch('time.time') as time:
            time.side_effect = [1000, 1001]

            with aioresponses() as http:
                http.get('https://foo.com', status=200, body='nothing here')

                result = event_loop.run_until_complete(self.job.run(target))

                assert result == HTTPCheckResult(url='https://foo.com',
                                                 status_code=200,
                                                 response_time=1000,
                                                 re_match=False,
                                                 error=None)

    def test_run_on_client_error(self, event_loop):
        target = Target(url='https://foo.com')

        with mock.patch('time.time') as time:
            time.side_effect = [1000, 1001]

            with aioresponses() as http:
                http.get('https://foo.com', exception=ClientError('Error connecting'))

                result = event_loop.run_until_complete(self.job.run(target))

                assert result == HTTPCheckResult(url='https://foo.com',
                                                 response_time=1000,
                                                 status_code=None,
                                                 re_match=None,
                                                 error="ClientError('Error connecting')")

