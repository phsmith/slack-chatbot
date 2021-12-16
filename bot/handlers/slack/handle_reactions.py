"""
Slack message reactions handler module
"""


class HandleReactions():
    """
    Class to handle slack message reactions
    """
    thread_ts = str

    def __init__(self, slack_client: object):
        slack_client.event("reaction_added")(self.handle_reactions_added)

    def handle_reactions_added(self, client: object, body: dict, event: dict) -> None:
        """Handle reactions on messages

        Args:
            client: Slack client instance
            event: Slack event trigger info
        """
        if not event:
            return

        if event["reaction"] == "eyes":
            client.chat_postMessage(
                blocks=[{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":eyes: <@{event['user']}> está de olho na sua solicitação!"
                    }
                }],
                text=f"<@{event['user']}> está de olho e logo irá responder!",
                channel=event["item"]["channel"],
                thread_ts=self.thread_ts
            )
