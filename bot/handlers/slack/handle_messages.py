"""
Slack messages handler module
"""


class HandleMessages():
    """
    Class to handle slack channel messages
    """
    def __init__(self, slack_client: object):
        slack_client.event("message")(self.handle_message)

    def handle_message(self, message: dict, say: object) -> None:
        """Handle messages from slack channel

        Args:
            message: Slack message object
            say: Slack client say function
        """

        bot_message = ":robot_face: Para suporte, favor utilizar o atalho */suporte*"

        if message.get("thread_ts"):
            return

        if not message.get("subtype") in [
            "bot_message",
            "channel_leave",
            "message_deleted",
            "message_changed"
        ]:
            say(bot_message)
            return bot_message
        else:
            return
