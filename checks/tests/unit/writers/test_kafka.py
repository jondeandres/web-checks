import mock

from checks.writers.kafka import Kafka
from checks.lib.result import Result

_TOPIC = 'test'


class TestKafka:
    def test_write(self):
        result1 = Result()
        result2 = Result()

        producer = mock.Mock()
        serializer = mock.Mock()
        serializer.dump.side_effect = ['foo', 'bar']

        writer = Kafka(producer, _TOPIC, serializer)

        writer.write([result1, result2])

        serializer.dump.assert_has_calls([
            mock.call(result1),
            mock.call(result2)
        ])

        producer.produce.assert_has_calls([
            mock.call('test', 'foo'),
            mock.call('test', 'bar')
        ])
        producer.flush.assert_called_once()
