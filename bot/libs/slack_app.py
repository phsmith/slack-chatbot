"""
Slack client module
"""

from slack_bolt import App
from bot.config import Config


class SlackApp(App):
    """
    Slack App instance class

    Returns:
        object: A slack_bolt App instance
    """

    def __init__(self):
        super().__init__(
            signing_secret=Config.slack_signing_secret,
            token=Config.slack_bot_token
        )

    def get_usergroups_id(self, usergroups: list = []) -> dict:
        usergroups_list = self.client.usergroups_list(types="public_channel,private_channel")
        output = dict()

        for usergroup in usergroups_list["usergroups"]:
            usergroup_id = usergroup["id"]
            usergroup_handle = usergroup["handle"]

            if usergroup_handle in usergroups:
                output.update({usergroup_handle: usergroup_id})

        return output
