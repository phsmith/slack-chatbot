"""
Configuration module
"""

import json
import os
import logging

from base64 import b64encode
from typing import Optional, Union
from jinja2 import (
    Environment,
    PackageLoader,
    TemplateNotFound,
    select_autoescape
)

# Logging configuration
logging.basicConfig(
    format="[%(asctime)s] [%(process)s] [%(levelname)s] %(filename)s:%(lineno)s:%(funcName)s() - %(message)s",
    datefmt="%F %T %z",
    level=logging.INFO
)


class Config:
    """
    Base configurations class

    Args:
        bot_listen_port: Bot listening http port. Default: 5000
        logger: Instance of logging to manage logs info
        template_env: Jinja2 templates dir environment
    """
    logger = logging.getLogger(__name__)
    port = os.environ.get('PORT', 5000)
    templates_env = Environment(
        loader=PackageLoader("bot"),
        autoescape=select_autoescape()
    )

    def load_template(self, template: str, **kwargs) -> Optional[Union[list, dict]]:
        """Load a jinja2 template file from templates dir

        Args:
            template: Template file name
            kwargs: Dict with keys/values that will be
                    replaced when template was loaded
        Returns:
            The template file content
        """
        try:
            template = self.templates_env.get_template(template)
            return json.loads(template.render(**kwargs), strict=False)
        except TemplateNotFound:
            return self.logger.error(f"Template {template} not found.")


class SlackConfig(Config):
    """Slack base configurations class

    Args:
        slack_bot_token: Bot token from https://api.slack.com/apps
        slack_bot_signing_secret: Bot signing secret token from https://api.slack.com/apps
        slack_channel: Slack conversation channel
        slack_templates: Dictionary to map templates.
                         Example: slack_templates["shortcuts"]["support"]
    """
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
    slack_channel = os.environ.get("SLACK_CHANNEL")
    slack_templates = {
        "shortcuts": {
            "support": "slack/shortcut_support.json"
        }
    }


class AzDevOpsConfig(Config):
    """Azure base configurations class

    Args:
        az_organization_url: Azure organization url
        az_personal_access_token: Azure Devops personal access token
        az_devops_project_board: Azure Boards project name
        az_devops_board_template: Azure Boards payload
    """
    az_devops_organization_url = os.environ.get("AZ_DEVOPS_ORGANIZATION_URL")
    az_devops_pat = os.environ.get("AZ_DEVOPS_PERSONAL_ACCESS_TOKEN")
    az_devops_pat_b64 = b64encode(f"'':{az_devops_pat}".encode()).decode()
    az_devops_project_board = os.environ.get("AZ_DEVOPS_PROJECT_BOARD")
    az_devops_worK_item_type = os.environ.get("AZ_DEVOPS_WORK_ITEM_TYPE", "Support")
    az_devops_board_template = f"azure_devops/{az_devops_project_board}.j2"
    az_devops_worK_item_iteration = os.environ.get("AZ_DEVOPS_WORK_ITEM_ITERATION", "")
    # AZ_DEVOPS_WORK_ITEM_AREA must be set like: AZ_DEVOPS_WORK_ITEM_AREA=\\Area1
    az_devops_worK_item_area = f'{az_devops_project_board}{os.environ.get("AZ_DEVOPS_WORK_ITEM_AREA", "")}'
