import asyncio
import mock

from checks.worker import Worker
from checks.lib.job import Job
from checks.lib.repository import Repository
from checks.lib.writer import Writer


class DummyJob:
    async def run(self, obj):
      return obj * 2


class TestWorker:
    def test_run(self, event_loop):
        repo = mock.Mock(spec=Repository)
        repo.get_objects.return_value = [1, 2, 3]

        job_future = asyncio.Future()
        job_future.set_result(1)
        job = mock.Mock()
        job.run.return_value = job_future

        writer = mock.Mock(spec=Writer)

        worker = Worker(job, repo, writer)
        event_loop.run_until_complete(worker.run())

        repo.get_objects.assert_called_with()
        job.run.assert_has_calls([
            mock.call(1),
            mock.call(2),
            mock.call(3)
        ])

        writer.write.assert_called_with([1, 1, 1])