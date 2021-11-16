from unittest import TestCase
from unittest.mock import patch

from bot.config import SlackConfig, AzDevOpsConfig
from bot.handlers.slack.handle_shortcut_support import HandleShortcutSupport


class TestHandleShortcutSupport(TestCase, SlackConfig, AzDevOpsConfig):
    @patch("bot.libs.slack_client.SlackClient")
    def setUp(self, mock_slack_client):
        AzDevOpsConfig.az_devops_organization_url = "https://dummy.azure.com"
        AzDevOpsConfig.az_devops_personal_access_token = "test"
        AzDevOpsConfig.az_devops_project_board = "test"
        SlackConfig.slack_channel = "test"

        mock_slack_client_attrs = {
            "users_info.return_value": dict(user=dict(name="TestUser")),
            "views_open.return_value": dict(user=dict(name="TestViewsOpen")),
            "users_conversations.return_value": dict(channels=[dict(id=1, name="test")])
        }
        mock_slack_client.configure_mock(**mock_slack_client_attrs)

        self.slack_client = mock_slack_client
        self.slack_message_body = {'type': 'view_submission', 'team': {'id': 'T02209CMMAM', 'domain': 'testdomain'}, 'user': {'id': 'U021JJDD405', 'username': 'phillipe.chaves', 'name': 'phillipe.chaves', 'team_id': 'T02209CMMAM'}, 'api_app_id': 'A02209FBKLZ', 'token': 'BQdiLmRmgeC6TkgwUppLLgRX', 'trigger_id': '2664724918786.2068318735361.1151d50a942a35eeef9e41abd66eb18e', 'view': {'id': 'V02KJMA380J', 'team_id': 'T02209CMMAM', 'type': 'modal', 'blocks': [{'type': 'input', 'block_id': 'rt6Jw', 'label': {'type': 'plain_text', 'text': 'Brief', 'emoji': True}, 'optional': False, 'dispatch_action': False, 'element': {'type': 'plain_text_input', 'action_id': 'title', 'placeholder': {'type': 'plain_text', 'text': 'Short summary', 'emoji': True}, 'dispatch_action_config': {'trigger_actions_on': ['on_enter_pressed']}}}, {'type': 'input', 'block_id': 'XL9', 'label': {'type': 'plain_text', 'text': 'Environment', 'emoji': True}, 'optional': False, 'dispatch_action': False, 'element': {'type': 'static_select', 'action_id': 'environment', 'placeholder': {'type': 'plain_text', 'text': 'Select an option', 'emoji': True}, 'options': [{'text': {'type': 'plain_text', 'text': 'Non-Production', 'emoji': True}, 'value': 'N-Production'}, {'text': {'type': 'plain_text', 'text': 'Production', 'emoji': True}, 'value': 'Production'}]}}, {'type': 'input', 'block_id': 'Hfq', 'label': {'type': 'plain_text', 'text': 'Infrastructure', 'emoji': True}, 'optional': False, 'dispatch_action': False, 'element': {'type': 'static_select', 'action_id': 'infrastructure', 'placeholder': {'type': 'plain_text', 'text': 'Select an option', 'emoji': True}, 'options': [{'text': {'type': 'plain_text', 'text': 'Azure', 'emoji': True}, 'value': 'Azure'}, {'text': {'type': 'plain_text', 'text': 'Ascenty', 'emoji': True}, 'value': 'Ascenty'}, {'text': {'type': 'plain_text', 'text': 'AWS', 'emoji': True}, 'value': 'AWS'}, {'text': {'type': 'plain_text', 'text': 'GCP', 'emoji': True}, 'value': 'GCP'}, {'text': {'type': 'plain_text', 'text': 'IBM Cloud', 'emoji': True}, 'value': 'IBM Cloud'}, {'text': {'type': 'plain_text', 'text': 'QTS Atlanta', 'emoji': True}, 'value': 'QTS Atlanta'}, {'text': {'type': 'plain_text', 'text': 'QTS Chicago', 'emoji': True}, 'value': 'QTS Chicago'}, {'text': {'type': 'plain_text', 'text': 'Tivit', 'emoji': True}, 'value': 'Tivit'}]}}, {'type': 'input', 'block_id': 'jEw', 'label': {'type': 'plain_text', 'text': 'Product', 'emoji': True}, 'optional': False, 'dispatch_action': False, 'element': {'type': 'static_select', 'action_id': 'product', 'placeholder': {'type': 'plain_text', 'text': 'Select an option', 'emoji': True}, 'options': [{'text': {'type': 'plain_text', 'text': 'Algobot', 'emoji': True}, 'value': 'Algobot'}, {'text': {'type': 'plain_text', 'text': 'Algosec', 'emoji': True}, 'value': 'Algosec'}, {'text': {'type': 'plain_text', 'text': 'FTPS', 'emoji': True}, 'value': 'FTPS'}, {'text': {'type': 'plain_text', 'text': 'Fileserver/DFS', 'emoji': True}, 'value': 'Fileserver/DFS'}, {'text': {'type': 'plain_text', 'text': 'Firewall', 'emoji': True}, 'value': 'Firewall'}, {'text': {'type': 'plain_text', 'text': 'Fortimanager', 'emoji': True}, 'value': 'Fortimanager'}, {'text': {'type': 'plain_text', 'text': 'IBM Connect Direct', 'emoji': True}, 'value': 'IBM Connect Direct'}, {'text': {'type': 'plain_text', 'text': 'Jump server', 'emoji': True}, 'value': 'Jump server'}, {'text': {'type': 'plain_text', 'text': 'KMS', 'emoji': True}, 'value': 'KMS'}, {'text': {'type': 'plain_text', 'text': 'Load Balancer', 'emoji': True}, 'value': 'Load Balancer'}, {'text': {'type': 'plain_text', 'text': 'Puppet/Foreman', 'emoji': True}, 'value': 'Puppet/Foreman'}, {'text': {'type': 'plain_text', 'text': 'Resolução de Nomes (DNS)', 'emoji': True}, 'value': 'Resolução de Nomes (DNS)'}, {'text': {'type': 'plain_text', 'text': 'Roteamento', 'emoji': True}, 'value': 'Roteamento'}, {'text': {'type': 'plain_text', 'text': 'Rundeck', 'emoji': True}, 'value': 'Rundeck'}, {'text': {'type': 'plain_text', 'text': 'SFTP', 'emoji': True}, 'value': 'SFTP'}, {'text': {'type': 'plain_text', 'text': 'SMTP Relay', 'emoji': True}, 'value': 'SMTP Relay'}, {'text': {'type': 'plain_text', 'text': 'Satellite/Katello', 'emoji': True}, 'value': 'Satellite/Katello'}, {'text': {'type': 'plain_text', 'text': 'Stack vRealize', 'emoji': True}, 'value': 'Stack vRealize'}, {'text': {'type': 'plain_text', 'text': 'VPN', 'emoji': True}, 'value': 'VPN'}, {'text': {'type': 'plain_text', 'text': 'Virtual Machine (VM)', 'emoji': True}, 'value': 'Virtual Machine (VM)'}, {'text': {'type': 'plain_text', 'text': 'WSUS', 'emoji': True}, 'value': 'WSUS'}, {'text': {'type': 'plain_text', 'text': 'vCenter', 'emoji': True}, 'value': 'vCenter'}]}}, {'type': 'input', 'block_id': 'RZYN', 'label': {'type': 'plain_text', 'text': 'Description', 'emoji': True}, 'optional': False, 'dispatch_action': False, 'element': {'type': 'plain_text_input', 'action_id': 'description', 'placeholder': {'type': 'plain_text', 'text': 'Request details', 'emoji': True}, 'multiline': True, 'dispatch_action_config': {'trigger_actions_on': ['on_enter_pressed']}}}], 'private_metadata': '', 'callback_id': '', 'state': {'values': {'rt6Jw': {'title': {'type': 'plain_text_input', 'value': 'Teste'}}, 'XL9': {'environment': {'type': 'static_select', 'selected_option': {'text': {'type': 'plain_text', 'text': 'Non-Production', 'emoji': True}, 'value': 'N-Production'}}}, 'Hfq': {'infrastructure': {'type': 'static_select', 'selected_option': {'text': {'type': 'plain_text', 'text': 'Azure', 'emoji': True}, 'value': 'Azure'}}}, 'jEw': {'product': {'type': 'static_select', 'selected_option': {'text': {'type': 'plain_text', 'text': 'Algobot', 'emoji': True}, 'value': 'Algobot'}}}, 'RZYN': {'description': {'type': 'plain_text_input', 'value': 'Teste'}}}}, 'hash': '1635515438.eLojbVh8', 'title': {'type': 'plain_text', 'text': 'TIS-Support', 'emoji': True}, 'clear_on_close': False, 'notify_on_close': False, 'close': {'type': 'plain_text', 'text': 'Cancel', 'emoji': True}, 'submit': {'type': 'plain_text', 'text': 'Send', 'emoji': True}, 'previous_view_id': None, 'root_view_id': 'V02KJMA380J', 'app_id': 'A02209FBKLZ', 'external_id': '', 'app_installed_team_id': 'T02209CMMAM', 'bot_id': 'B021MT5SV3M'}, 'response_urls': [], 'is_enterprise_install': False, 'enterprise': None}
        self.slack_handle_support = HandleShortcutSupport(self.slack_client)

    def test_handle_shortcut(self):
        self.slack_handle_support.handle_shortcut(
            print, self.slack_message_body, self.slack_client
        )

        self.slack_client.views_open.assert_called_once_with(
            trigger_id=self.slack_message_body["trigger_id"],
            view=self.load_template(self.slack_templates["shortcuts"]["support"])
        )

    # @patch("bot.libs.az_devops_client.AzDevOpsClient")
    @patch("bot.libs.az_devops_client.AzDevOpsClient.connect")
    @patch("bot.libs.az_devops_client.AzDevOpsClient.get_team_settings")
    def test_handle_shortcut_submission(self, mock_az_devops_team_settings, mock_az_devops_client_connect):
        mock_az_devops_team_settings.return_value = {
            "defaultIteration": {
                "path": "\\Test"
            }
        }

        self.slack_handle_support.handle_shortcut_submission(
            print, self.slack_message_body, self.slack_client, self.logger
        )
