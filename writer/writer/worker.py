import logging


from writer.lib.kafka.consumer import Consumer
from writer.lib.job import Job
from writer.lib.deserializer import Deserializer

_BATCH_SIZE = 5


log = logging.getLogger(__name__)


class Worker:
    def __init__(self, consumer: Consumer, job: Job, deserializer: Deserializer):
        self.__consumer = consumer
        self.__job = job
        self.__deserializer = deserializer
        self.__is_running = False

    def start(self) -> None:
        self.__consumer.subscribe()
        self.__is_running = True

    def stop(self) -> None:
        self.__is_running = False

    def run(self) -> None:
        while self.__is_running:
            messages = self.__consumer.consume(_BATCH_SIZE)

            if not messages:
                self.__consumer.commit()

                continue

            log.info(
                'Running job %s for %d messages',
                type(self.__job).__name__,
                len(messages)
            )
            self.__job.run(self.__deserializer.loads(msg)
                           for msg in messages)

            self.__consumer.commit()

        self.__consumer.stop()