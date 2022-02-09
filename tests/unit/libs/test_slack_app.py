from unittest import TestCase
from unittest.mock import patch

from bot.config import Config
from bot.libs.slack_app import SlackApp


class TestSlackApp(TestCase):
    def setUp(self):
        Config.slack_bot_token = "test"
        Config.slack_signing_secret = "test"

    @patch("bot.libs.slack_app.App.__init__")
    def test_slack_app(self, mock_slack_app):
        slack_app = SlackApp()

        mock_slack_app.assert_called_once_with(
            signing_secret="test",
            token="test"
        )

        assert slack_app is not None
