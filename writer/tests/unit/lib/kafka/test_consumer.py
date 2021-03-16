import mock

from writer.lib.kafka.consumer import Consumer


class TestConsumer:
    @mock.patch('writer.lib.kafka.consumer.ConfluentConsumer')
    def test_consume(self, ConfluentConsumer):
        # Mocking whole class since mock cannot set
        # properties in cimpl.Consumer
        confluent_consumer = ConfluentConsumer.return_value
        message1 = mock.Mock()
        message1.value.return_value = 'foo'

        message2 = mock.Mock()
        message2.value.return_value = 'bar'

        confluent_consumer.consume.return_value = [message1, message2]

        consumer = Consumer(['topic'],
                            {'brokers': ['kafka'], 'group_id': 'tests'})

        result = consumer.consume(100, timeout=5)

        assert result == ['foo', 'bar']
        confluent_consumer.consume.assert_called_with(100, timeout=5)
