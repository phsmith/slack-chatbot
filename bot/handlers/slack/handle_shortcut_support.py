"""
Slack handle shortcut support module
"""
from bot.config import Config
from bot.libs.az_devops_client import AzDevOpsClient
from bot.handlers.slack.handle_reactions import HandleReactions


class HandleShortcutSupport(HandleReactions):
    """ Class to handle slack channel support shortcut

    Attributes:
        callback_id: Slack shortcut callback_id
    """
    callback_id = None

    def __init__(self, slack_client: object):
        self.shortcut_config = Config.slack_shortcuts[self.callback_id]
        slack_client.shortcut(self.callback_id)(self.handle_shortcut)
        slack_client.view_submission("")(self.handle_shortcut_submission)
        super().__init__(slack_client)

    def handle_shortcut(self, ack: object, client: object, shortcut: dict) -> None:
        """Handle shortcut modal view openning

        Args:
            ack: Acknowledge the command request
            client: Slack client instance
            shortcut: Slack shortcut trigger info
        """
        ack()

        client.views_open(
            trigger_id=shortcut["trigger_id"],
            view=Config.load_template(
                self.shortcut_config["slack_template"]
            )
        )

    def handle_shortcut_submission(
        self, ack: object, body: dict, client: object,
        event: dict, logger: object
    ) -> None:
        """Handle shortcut modal view submission

        Args:
            ack: Acknowledge the command request
            body: Slack message body info
            client: Slack client instance
            event: Slack events info
            logger: Logging instance
        """
        ack()

        az_devops_client = AzDevOpsClient()
        az_devops_team_settings = az_devops_client.get_team_settings(self.shortcut_config["az_devops_project"])

        # view_blocks = list(map(lambda x: x["block_id"], body["view"]["blocks"]))
        view_state_values = body["view"]["state"]["values"]

        user_name = body["user"]["name"]
        title = view_state_values["title_block"]["title"]["value"].replace('"', "'")
        environment = view_state_values["environment_block"]["environment"]["selected_option"]["value"]
        infrastructure = view_state_values["infrastructure_block"]["infrastructure"]["selected_option"]["value"]
        product = view_state_values["product_block"]["product"]["selected_option"]["value"]
        description = view_state_values["description_block"]["description"]["value"].replace('"', "'")
        bot_message = (
            f"*Resumo da Solicitação:* {title}\n"
            f"*Ambiente:* {environment}\n"
            f"*Infraestrutura:* {infrastructure}\n"
            f"*Produto ou Serviço:* {product}\n"
            f"*Informações Complementares:* {description}"
        )

        # Get bot user_id and channels that it's subscribed
        bot_id = body["view"]["bot_id"]
        bot_user_id = client.bots_info(bot=bot_id).get("bot").get("user_id")
        bot_subscribed_channels = client.users_conversations(user=bot_user_id).get("channels", [])

        # Verifying if bot is subscribed in the slack channel
        # specified in config.py
        channel_id = None
        channels_filter = list(
            filter(
                lambda chn: chn["id"] if chn["name"] == self.shortcut_config["slack_channel"] else None,
                bot_subscribed_channels
            )
        )

        if channels_filter:
            channel_id = channels_filter[0]["id"]
        else:
            raise ValueError(f"Bot not subscribed in the channel #{self.shortcut_config['slack_channel']}.")

        # Posts a message in the channel with the support form data
        post_message = client.chat_postMessage(
            text=f"*Solicitante:* <@{user_name}>\n{bot_message}",
            channel=channel_id
        )

        # Manage reactions in the thread
        HandleReactions.thread_ts = post_message["ts"]

        logger.info(
            f"New message received on channel #{self.shortcut_config['slack_channel']} from "
            f"{user_name}: {repr(bot_message)}"
        )

        client.chat_postMessage(
            blocks=[{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (f":eyes: O time está de olho e logo irá responder...\n"
                             f"O SLA de Atendimento é de *{self.shortcut_config['az_devops_sla'][environment]}*.")
                }
            }],
            text=(f"O time está de olho e logo irá responder... "
                  f"O SLA de Atendimento é de {self.shortcut_config['az_devops_sla'][environment]}."),
            channel=channel_id,
            thread_ts=post_message["ts"]
        )

        # Get the thread permanent link
        thread_link = client.chat_getPermalink(
            channel=channel_id,
            message_ts=post_message["ts"]
        )

        try:
            # Creates a card on Azure DevOps Boards
            board_item = az_devops_client.add_item_to_project_board(
                work_item_type=self.shortcut_config["az_devops_work_item_type"],
                project=self.shortcut_config["az_devops_project"],
                document=Config.load_template(
                    template=self.shortcut_config["az_devops_board_template"],
                    title=title,
                    description=(
                        f"<b>Solicitante:</b> {user_name}<br/>"
                        f"<b>Referência:</b> <a href='{thread_link.get('permalink')}'>Link da thread</a>"
                        f"<br/><br/>{description}"
                    ),
                    environment=environment,
                    infrastructure=infrastructure,
                    product=product,
                    area_path=self.shortcut_config["az_devops_work_item_area"],
                    iteration_path=self.shortcut_config["az_devops_work_item_iteration"] or (
                        f'{self.shortcut_config["az_devops_project"]}'
                        f'\\{az_devops_team_settings["defaultIteration"]["path"]}'
                    )
                )
            )

            board_item_url = (
                f"{Config.az_devops_organization_url}"
                f"/{self.shortcut_config['az_devops_project']}"
                f"/_workitems/edit/{board_item.id}"
            )

            client.chat_postMessage(
                blocks=[{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":azure_board: O seguinte card de suporte foi criado: <{board_item_url}|#{board_item.id}>"
                    }
                }],
                text=f"O seguinte card de suporte foi criado: <{board_item_url}|#{board_item.id}>",
                channel=channel_id,
                thread_ts=post_message["ts"]
            )
        except Exception:
            logger.error("Failed to create Azure Boards Work Item.", exc_info=True)
