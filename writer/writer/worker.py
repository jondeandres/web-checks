from writer.lib.kafka.consumer import Consumer
from writer.lib.job import Job
from writer.lib.deserializer import Deserializer

_BATCH_SIZE = 5


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
            self.__job.run(self.__deserializer.loads(msg)
                           for msg in self.__consumer.consume(_BATCH_SIZE))

            self.__consumer.commit()

        self.__consumer.stop()