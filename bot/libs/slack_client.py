"""
Slack client module
"""

from slack_bolt import App
from bot.config import SlackConfig


class SlackClient(SlackConfig):
    """
    Slack client instance class

    Returns:
        app: A slack_bolt App instance
    """
    def __init__(self):
        self.app = App(
            signing_secret=self.slack_signing_secret,
            token=self.slack_bot_token
        )
