"""
Azure DevOps client module
"""

import requests

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

from bot.config import Config

requests.urllib3.disable_warnings()


class AzDevOpsClient():
    """
    Class that provides a wrapper for the Azure DevOps Python API
    More info at https://github.com/microsoft/azure-devops-python-api
    """

    def __init__(self):
        self.connection = self.connect()
        self.work_item_tracking_client = None

    def connect(self) -> object:
        """Cretes a new connection with on Azure Devops

        Returns:
            The connection object
        """
        credentials = BasicAuthentication('', Config.az_devops_pat)
        connection = Connection(base_url=Config.az_devops_organization_url, creds=credentials)
        return connection

    def provide_work_item_tracking_client(self) -> object:
        """Set work_item_tracking_client
           to communicates with Azure DevOps Boards
        """
        self.work_item_tracking_client = self.connection.clients.get_work_item_tracking_client()

    def get_team_settings(self, project: str) -> dict:
        """Get team_settings"""

        team_settings_url = (
            f"{Config.az_devops_organization_url}/{project}"
            "/_apis/work/teamsettings?api-version=6.1-preview.1"
        )

        request = requests.get(
            url=team_settings_url,
            headers={"Authorization": f"Basic {Config.az_devops_pat_b64}"},
            verify=False
        )

        try:
            return request.json()
        except Exception:
            message = f"{request.status_code} {request.reason}: {request.url}"
            Config.logger.error(message)
            return

    def add_item_to_project_board(
        self, project: str, document: list, work_item_type: str
    ) -> dict:
        """Add new items to Azure DevOps Boards

        Reference: https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/work%20items/create?view=azure-devops-rest-6.1

        Args:
            project: Project name
            document: Work item document template.
            work_item_type: Work item type. Example: Support

        Retuns:
            The board item created
        """
        if not self.work_item_tracking_client:
            self.provide_work_item_tracking_client()

        if not project or not work_item_type:
            raise ValueError("project and work_item_type must be set.")

        try:
            board_item = self.work_item_tracking_client.create_work_item(
                project=project,
                type=work_item_type,
                document=document
            )

            return board_item
        except Exception as error:
            Config.logger.error(str(error))

    def update_work_item(
        self, project: str, document: list, work_item_id: str
    ) -> dict:
        """Update an work item on Azure DevOps Boards

        Args:
            project: Project name
            document: Work item document template
            work_item_id: Work item id to update

        Retuns:
            The board item updated
        """
        if not self.work_item_tracking_client:
            self.provide_work_item_tracking_client()

        if not project or not document or not work_item_id:
            raise ValueError("project, document and work_item_id must be set.")

        try:
            updated_board_item = self.work_item_tracking_client.update_work_item(
                project=project,
                document=document,
                id=work_item_id
            )

            return updated_board_item
        except Exception as error:
            Config.logger.error(str(error))
