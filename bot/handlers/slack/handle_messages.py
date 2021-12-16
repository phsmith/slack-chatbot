"""
Slack messages handler module
"""

from bot.config import Config


class HandleMessages():
    """
    Class to handle slack channel messages
    """
    def __init__(self, slack_client: object):
        slack_client.event("message")(self.handle_message)

    def handle_message(self, client: object, message: dict, say: object) -> None:
        """Handle messages from slack channel

        Args:
            client: Slack client instance
            message: Slack message object
            say: Slack client say function
        """

        channel_info = client.conversations_info(channel=message["channel"])["channel"]
        channel_shortcuts_list = Config.get_channel_shortcuts(channel_info["name"])
        channel_shortcuts = ', '.join(map(lambda x: '/' + x, channel_shortcuts_list))
        bot_message = f":robot_face: Para suporte, favor utilizar o(s) atalho(s): *{channel_shortcuts}*"

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
            say(bot_message)
            return bot_message
        else:
            return
