"""
Slack messages handler module
"""

from bot.config import Config
from bot.handlers.slack.handle_reactions import HandleReactions

class HandleMessages(HandleReactions):
    """
    Class to handle slack channel messages
    """

    def __init__(self, slack_app: object):
        slack_app.event("message")(self.handle_message)
        super().__init__(slack_app)

    def handle_message(self, client: object, message: dict, say: object) -> None:
        """Handle messages from slack channel

        Args:
            client: Slack App instance
            message: Slack message object
            say: Slack client say function
        """

        channel_info = client.conversations_info(channel=message["channel"])["channel"]
        channel_shortcuts_list = Config.get_channel_shortcuts(channel_info["name"])
        channel_shortcuts = ", ".join(map(lambda x: "/" + x, channel_shortcuts_list))
        bot_message_text = (
            f":robot_face: Para suporte, favor utilizar o(s) atalho(s): "
            f"*{channel_shortcuts}* e preencha o formulário correspondente."
        )

        if message.get("thread_ts"):
            return

        if not message.get("subtype") in [
            "bot_message",
            "channel_leave",
            "channel_join",
            "channel_topic",
            "channel_purpose",
            "message_deleted",
            "message_changed"
        ]:
            say(bot_message_text)

            return bot_message_text

        return
