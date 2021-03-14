import asyncio
import time

from checks.lib.job import Job
from checks.lib.repository import Repository
from checks.lib.writer import Writer


_DEFAULT_PERIOD = 5


class Worker:
    """
    Service class that orchestrates the interaction between
    the data source and output

    For each object returned by the Repository it'll call the
    received Job. The collected result is used to call the Writer.

    """
    def __init__(self, job: Job, repository: Repository, writer: Writer, period: int = _DEFAULT_PERIOD):
        """
        Args:
          job: A Job that implements the logic to execute per received object
          repository: A Repository that abtracts the data input
          writer: A Writer that handles the data output
        """
        self.__job = job
        self.__repository = repository
        self.__writer = writer
        self.__last_run = 0
        self.__period = period
        self.__is_running = True

    def stop(self):
        self.__is_running = False

    async def run(self) -> None:
        while self.__is_running:
            if self.__should_run():
                results = await asyncio.gather(*[
                        self.__job.run(obj)
                        for obj in self.__repository.get_objects()
                ])

                self.__writer.write(results)
                self.__last_run = time.time()
            else:
                time.sleep(1)

    def __should_run(self) -> bool:
        return self.__last_run < (time.time() - self.__period)
