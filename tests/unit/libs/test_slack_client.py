from unittest import TestCase
from unittest.mock import patch

from bot.config import Config
from bot.libs.slack_client import SlackClient


class TestSlackClient(TestCase):
    def setUp(self):
        Config.slack_bot_token = 'test'
        Config.slack_signing_secret = 'test'

    @patch("bot.libs.slack_client.App", autospec=True)
    def test_slack_client(self, mock_slack_client):
        slack_client = SlackClient()

        mock_slack_client.assert_called_once_with(
            signing_secret="test",
            token="test"
        )

        assert slack_client is not None
