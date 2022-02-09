import unittest
from unittest.mock import patch
from bot.libs.az_devops_client import AzDevOpsClient


class TestAzDevOpsClient(unittest.TestCase):
    @patch("bot.libs.az_devops_client.AzDevOpsClient.connect")
    def setUp(self, mock_az_devops_client):
        AzDevOpsClient.az_devops_organization_url = "https://dummy.azure.com"
        self.project = "inf-core-dc-compute"
        self.work_item_type = "Support"
        self.az_devops_client = AzDevOpsClient()

    def test_add_item_to_project_board(self):
        self.az_devops_client.add_item_to_project_board(
            project=self.project,
            work_item_type=self.work_item_type,
            document={}
        )

        self.az_devops_client.work_item_tracking_client.create_work_item.assert_called_with(
            project=self.project,
            type=self.work_item_type,
            document={}
        )

    def test_add_item_to_project_board_wrong_project(self):
        self.assertRaises(
            ValueError,
            self.az_devops_client.add_item_to_project_board,
            project=None,
            work_item_type=self.work_item_type,
            document={}
        )
