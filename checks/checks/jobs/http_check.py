import math
import re
import time

import aiohttp
from aiohttp.client_exceptions import ClientError

from checks.lib.job import Job
from checks.model.target import Target
from checks.model.http_check_result import HTTPCheckResult


class HTTPCheck(Job):
    """
    HTTP check job
    """
    async def run(self, target: Target) -> HTTPCheckResult:
        """
        It performs get requests to received target's URL and returns a result
        with the response time, status code, URL, regex match result and error,
        if any.
        """
        async with aiohttp.ClientSession() as session:
            start_time = time.time()

            try:
                async with session.get(target.url) as response:
                    re_match = None

                    if target.regex:
                        re_match = bool(target.regex and
                                        re.match(target.regex,
                                                 await response.text())
                                        is not None)

                    return HTTPCheckResult(url=target.url,
                                           response_time=self._floor_to_milliseconds(
                                               time.time() - start_time
                                            ),
                                           status_code=response.status,
                                           re_match=re_match)
            except ClientError as exc:
                return HTTPCheckResult(url=target.url,
                                       response_time=self._floor_to_milliseconds(
                                           time.time() - start_time
                                       ),
                                       error=repr(exc))

    @staticmethod
    def _floor_to_milliseconds(seconds: float) -> int:
        return math.floor(seconds * 1000)
