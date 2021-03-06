from unittest import TestCase
from unittest.mock import patch

from bot.handlers.slack.handle_messages import HandleMessages


class TestHandleMessages(TestCase):
    @patch("bot.libs.slack_app")
    def setUp(self, mock_slack_app):
        self.slack_app = mock_slack_app
        self.slack_message_handle = HandleMessages(self.slack_app)

    def test_handle_message_with_thread(self):
        slack_message = dict(
            channel="Test",
            subtype="bot_message",
            text="Test",
            thread_ts="0123456789"
        )

        self.assertIsNone(
            self.slack_message_handle.handle_message(self.slack_app, slack_message, print)
        )

    def test_handle_message_without_thread(self):
        slack_message = dict(
            channel="Test",
            subtype="user_message",
            text="Test"
        )

        self.assertIn(
            ":robot_face: Para suporte, favor utilizar o(s) atalho(s)",
            self.slack_message_handle.handle_message(
                self.slack_app, slack_message, print
            )
        )
