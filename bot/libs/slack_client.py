"""
Slack client module
"""

from slack_bolt import App
from bot.config import Config


class SlackClient():
    """
    Slack client instance class

    Returns:
        object: A slack_bolt App instance
    """
    def __new__(self):
        return App(
            signing_secret=Config.slack_signing_secret,
            token=Config.slack_bot_token
        )
