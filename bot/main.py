"""
Slack ChatBot
"""
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

from bot.libs.slack_client import SlackClient
from bot.handlers.slack.handle_messages import HandleMessages
from bot.handlers.slack.handle_shortcut_support import HandleShortcutSupport

# Flask App
app = Flask(__name__)

# Slack Client
slack_client = SlackClient()
slack_handle_messages = HandleMessages(slack_client.app)
slack_handle_shortcut_support = HandleShortcutSupport(slack_client.app)
slack_request_handler = SlackRequestHandler(slack_client.app)


@app.route("/slack/events", methods=["POST"])
def slack_events():
    return slack_request_handler.handle(request)


@app.route('/health', methods=['GET', 'POST'])
def healthcheck():
    return 'Bot is running!!!\n', 200


if __name__ == "__main__":
    app.run(port=slack_client.port)
