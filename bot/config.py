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
        port: Bot listening http port. Default: 5000
        logger: Instance of logging to manage logs info
        template_env: Jinja2 templates dir environment
        az_organization_url: Azure organization url
        az_devops_pat: Azure Devops personal access token
        slack_bot_token: Bot token from https://api.slack.com/apps
        slack_signing_secret: Bot signing secret token from https://api.slack.com/apps
        slack_shortcuts: Slack shortcuts configurations
    """
    logger = logging.getLogger(__name__)
    port = os.environ.get('PORT', 5000)
    templates_env = Environment(
        loader=PackageLoader("bot"),
        autoescape=select_autoescape()
    )

    @classmethod
    def load_template(cls, template: str, **kwargs) -> Optional[Union[list, dict]]:
        """Load a jinja2 template file from templates dir

        Args:
            template: Template file name
            kwargs: Dict with keys/values that will be
                    replaced when template was loaded
        Returns:
            The template file content
        """
        try:
            template = cls.templates_env.get_template(template)
            return json.loads(template.render(**kwargs), strict=False)
        except TemplateNotFound:
            return cls.logger.error(f"Template {template} not found.")

    @classmethod
    def get_channel_shortcuts(cls, channel_name: str) -> list:
        """Get the shortcuts associated to a Slack Channel

        Args:
            channel_name: The channel name

        Returns:
            A list with shortcuts names
        """
        channel_shortcuts = list()

        try:
            for shortcut in cls.slack_shortcuts:
                if cls.slack_shortcuts[shortcut].get("slack_channel") == channel_name:
                    channel_shortcuts.append(shortcut)
            return channel_shortcuts
        except Exception:
            cls.logger.error(f"No shortcuts found for channel {channel_name}", exc_info=True)

    # Azure DevOps configurations
    az_devops_organization_url = os.environ.get("AZ_DEVOPS_ORGANIZATION_URL")
    az_devops_pat = os.environ.get("AZ_DEVOPS_PERSONAL_ACCESS_TOKEN")
    az_devops_pat_b64 = b64encode(f"'':{az_devops_pat}".encode()).decode()

    # Slack configurations
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
    slack_shortcuts = {
        "devops_support": {
            "az_devops_board": "devops",
            "az_devops_board_template": "azure_devops/devops_team.j2",
            "az_devops_project": "devops-project",
            "az_devops_work_item_type": "Support",
            "az_devops_work_item_area": "devops-project\\\\q1",
            "az_devops_work_item_iteration": "",
            "az_devops_sla": {
                "N-Production": "5 days",
                "Production": "3 days"
            },
            "slack_channel": "devops-support",
            "slack_template": "slack/devops_shortcut_support.json"
        },
        "coud_support": {
            "az_devops_board": "cloud",
            "az_devops_board_template": "azure_devops/cloud_team.j2",
            "az_devops_project": "cloud-project",
            "az_devops_work_item_type": "Support",
            "az_devops_work_item_area": "cloud-project\\\\q1",
            "az_devops_work_item_iteration": "",
            "az_devops_sla": {
                "N-Production": "5 days",
                "Production": "3 days"
            },
            "slack_channel": "cloud-support",
            "slack_template": "slack/cloud_shortcut_support.json"
        }
    }
