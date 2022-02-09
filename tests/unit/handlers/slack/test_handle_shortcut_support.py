import json

from unittest import TestCase
from unittest.mock import patch

from bot.config import Config
from bot.handlers.slack.handle_shortcut_support import HandleShortcutSupport


class TestHandleShortcutSupport(TestCase):
    @patch("bot.libs.slack_app.SlackApp")
    def setUp(self, mock_slack_app):
        HandleShortcutSupport.callback_id = "test"
        Config.slack_shortcuts = {
            "test": {
                "az_devops_board": "test",
                "az_devops_board_template": "azure_devops/test.j2",
                "az_devops_project": "technology-infrastructure-services",
                "az_devops_work_item_type": "Support",
                "az_devops_work_item_area": "test\\\\Q1",
                "az_devops_work_item_iteration": "",
                "az_devops_sla": {
                    "N-Production": "3 dias",
                    "Production": "5 dias"
                },
                "slack_channel": "test",
                "slack_template": "slack/tis-administration_shortcut_support.json"
            }
        }
        Config.az_devops_organization_url = "https://dummy.azure.com"
        Config.az_devops_personal_access_token = "test"

        mock_slack_app_attrs = {
            "users_info.return_value": dict(user=dict(name="TestUser")),
            "views_open.return_value": dict(user=dict(name="TestViewsOpen")),
            "users_conversations.return_value": dict(
                channels=[dict(id=1, name="test")]
            )
        }
        mock_slack_app.configure_mock(**mock_slack_app_attrs)

        self.slack_app = mock_slack_app
        self.slack_message_body = json.load(open("tests/unit/slack_message_body.json"))
        self.slack_handle_support = HandleShortcutSupport(self.slack_app)

    def test_handle_shortcut(self):
        self.slack_handle_support.handle_shortcut(
            print, self.slack_app, self.slack_message_body, print
        )

        self.slack_app.views_open.assert_called_once_with(
            trigger_id=self.slack_message_body["trigger_id"],
            view=Config.load_template(Config.slack_shortcuts["test"]["slack_template"])
        )

    # @patch("bot.libs.az_devops_client.AzDevOpsClient")
    @patch("bot.libs.az_devops_client.AzDevOpsClient.connect")
    @patch("bot.libs.az_devops_client.AzDevOpsClient.get_team_settings")
    def test_handle_shortcut_submission(
        self, mock_az_devops_team_settings, mock_az_devops_client_connect
    ):
        self.event = dict()
        mock_az_devops_team_settings.return_value = {
            "defaultIteration": {
                "path": "\\Test"
            }
        }

        self.slack_handle_support.handle_shortcut_submission(
            print, self.slack_message_body, self.slack_app, self.event, Config.logger
        )
