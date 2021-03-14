import mock

from checks.lib.kafka.config import Config
from checks.lib.kafka.confluent_producer import ConfluentProducer


class TestConfluentProducer:
    # Mocking whole class since we can't seta property on cimpl.Producer
    @mock.patch('confluent_kafka.Producer')
    def test_produce(self, producer_cls):
        impl_producer = producer_cls.return_value
        producer = ConfluentProducer(Config(brokers=['kafka01:9092']))

        producer.produce('topic', 'value')

        impl_producer.produce.assert_called_once_with(topic='topic', value='value')
