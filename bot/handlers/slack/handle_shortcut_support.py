"""
Slack handle shortcut support module
"""
from bot.config import SlackConfig, AzDevOpsConfig
from bot.libs.az_devops_client import AzDevOpsClient


class HandleShortcutSupport(SlackConfig, AzDevOpsConfig):
    """
    Class to handle slack channel support shortcut
    """
    def __init__(self, slack_client: object):
        slack_client.shortcut("support")(self.handle_shortcut)
        slack_client.view_submission("")(self.handle_shortcut_submission)

    def handle_shortcut(self, ack: object, body: dict, client: object) -> None:
        """Handle shortcut modal view openning

        Args:
            ack: Acknowledge the command request
            body: Slack message body data
            client: Slack client instance
        """
        ack()

        client.views_open(
            trigger_id=body["trigger_id"],
            view=self.load_template(self.slack_templates["shortcuts"]["support"])
        )

    def handle_shortcut_submission(
        self, ack: object, body: dict, client: object, logger: object
    ) -> None:
        """Handle shortcut modal view submission

        Args:
            ack: Acknowledge the command request
            body: Slack message body data
            client: Slack client instance
            logger: Logging instance
        """
        ack()

        az_devops_client = AzDevOpsClient()

        view_blocks = list(map(lambda x: x["block_id"], body["view"]["blocks"]))
        view_state_values = body["view"]["state"]["values"]

        user_name = body["user"]["name"]
        title = view_state_values[view_blocks[0]]["title"]["value"]
        environment = view_state_values[view_blocks[1]]["environment"]["selected_option"]["value"]
        infrastructure = view_state_values[view_blocks[2]]["infrastructure"]["selected_option"]["value"]
        product = view_state_values[view_blocks[3]]["product"]["selected_option"]["value"]
        description = view_state_values[view_blocks[4]]["description"]["value"]
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
                lambda chn: chn["id"] if chn["name"] == self.slack_channel else None,
                bot_subscribed_channels
            )
        )

        if channels_filter:
            channel_id = channels_filter[0]["id"]
        else:
            raise ValueError(f"Bot not subscribed in the channel #{self.slack_channel}.")

        # Posts a message in the channel with the support form data
        post_message = client.chat_postMessage(
            text=f"*Requester:* <@{user_name}>\n{bot_message}",
            channel=channel_id
        )

        logger.info(
            f"New message received on channel #{self.slack_channel} from "
            f"{user_name}: {repr(bot_message)}"
        )

        client.chat_postMessage(
            blocks=[{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":eyes: O time está de olho e logo irá responder...\nO SLA de Atendimento é de *3 dias*."
                }
            }],
            text="O time está de olho e logo irá responder...O SLA de Atendimento é de 3 dias.",
            channel=channel_id,
            thread_ts=post_message["ts"]
        )

        # Get the thread permanent link
        thread_link = client.chat_getPermalink(
            channel=channel_id,
            message_ts=post_message["ts"]
        )

        # Creates a card on Azure DevOps Boards
        az_devops_team_settings = az_devops_client.get_team_settings()

        board_item = az_devops_client.add_item_to_project_board(
            work_item_type=self.az_devops_worK_item_type,
            project=az_devops_client.az_devops_project_board,
            document=self.load_template(
                template=self.az_devops_board_template,
                title=title,
                description=(
                    f"<b>Solicitante:</b> {user_name}<br/>"
                    f"<b>Referência:</b> <a href='{thread_link.get('permalink')}'>Link da thread</a>"
                    f"<br/><br/>{description}"
                ),
                environment=environment,
                infrastructure=infrastructure,
                product=product,
                area_path=self.az_devops_worK_item_area,
                iteration_path=self.az_devops_worK_item_iteration or (
                    f'{self.az_devops_project_board}'
                    f'\\{az_devops_team_settings["defaultIteration"]["path"]}'
                )
            )
        )

        board_item_url = (
            f"{self.az_devops_organization_url}"
            f"/{self.az_devops_project_board}"
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
