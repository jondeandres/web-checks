import asyncio

from checks.lib.job import Job
from checks.lib.repository import Repository
from checks.lib.writer import Writer


class Worker:
    """
    Service class that orchestrates the interaction between
    the data source and output

    For each object returned by the Repository it'll call the
    received Job. The collected result is used to call the Writer.

    """
    def __init__(self, job: Job, repository: Repository, writer: Writer):
        """
        Args:
          job: A Job that implements the logic to execute per received object
          repository: A Repository that abtracts the data input
          writer: A Writer that handles the data output
        """
        self.__job = job
        self.__repository = repository
        self.__writer = writer

    async def run(self) -> None:
        results = await asyncio.gather(*[
                self.__job.run(obj)
                for obj in self.__repository.get_objects()
        ])

        self.__writer.write(results)
