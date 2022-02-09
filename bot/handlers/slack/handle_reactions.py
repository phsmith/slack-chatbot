"""
Slack message reactions handler module
"""

from bot.config import Config

class HandleReactions:
    """
    Class to handle slack message reactions
    """

    def __init__(self, slack_app: object):
        slack_app.event("reaction_added")(self.handle_reactions_added)

    def handle_reactions_added(self, client: object, body: dict, event: dict, logger: Config.logger) -> None:
        """Handle reactions on messages

        Args:
            client: Slack App instance
            event: Slack event trigger info
        """

        if not event:
            return

        try:
            oldest_thread_reply = client.conversations_replies(
                channel=event["item"]["channel"],
                ts=event["item"]["ts"],
                limit=1
            )
            parent_thread_ts = oldest_thread_reply["messages"][0]["thread_ts"]

            if event["reaction"] == "eyes":
                client.chat_postMessage(
                    text=f":eyes: <@{event['user']}> está de olho na sua solicitação!",
                    channel=event["item"]["channel"],
                    thread_ts=parent_thread_ts
                )
        except Exception as error:
            logger.error(f"Error: failed to process the reaction: {event['reaction']}", exc_info=True)
