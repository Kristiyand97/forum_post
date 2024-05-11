import unittest
from unittest.mock import patch
from data.schemas import Message
from services.message_services import create_message
from services.message_services import insert_query

FAKE_INSERT_QUERY_VALUE = 1
MESSAGE_CONTENT = 'test'
MESSAGE_RECEIVER_ID = 1
MESSAGE_SENDER_ID = 2


class TestMessageServices(unittest.TestCase):
    @patch('services.message_services.insert_query')
    def test_create_message_correctly(self, mocked_insert_query):
        mocked_insert_query.return_value = FAKE_INSERT_QUERY_VALUE

        result = create_message(MESSAGE_CONTENT, MESSAGE_RECEIVER_ID, MESSAGE_SENDER_ID)

        self.assertIsInstance(result, Message)
        self.assertEqual(result.id, FAKE_INSERT_QUERY_VALUE)
        self.assertEqual(result.content, MESSAGE_CONTENT)
        self.assertEqual(result.sender_id, MESSAGE_SENDER_ID)
        self.assertEqual(result.receiver_id, MESSAGE_RECEIVER_ID)


if __name__ == '__main__':
    unittest.main()