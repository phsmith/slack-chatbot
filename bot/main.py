"""
Slack Chat Bot
"""
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

from bot.libs.slack_client import SlackClient
from bot.handlers.slack.handle_messages import HandleMessages
from bot.handlers.slack.handle_shortcut_support import HandleShortcutSupport

app = Flask(__name__)
slack_client = SlackClient()


# Slack Handles
@slack_client.middleware
def manage_request(body, next):
    """
    Method to intercepts Slack events before goes to handles
    """
    HandleMessages(slack_client)

    if body.get("type") == "shortcut":
        HandleShortcutSupport.callback_id = body["callback_id"]
        HandleShortcutSupport(slack_client)

    return next()


@app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Method that handles Slack events and send to Flask
    """
    return SlackRequestHandler(slack_client).handle(request)


@app.route('/health', methods=['GET', 'POST'])
def healthcheck():
    return 'Bot is running!!!\n', 200


if __name__ == "__main__":
    app.run(port=slack_client.port)
