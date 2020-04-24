#!/bin/bash

cat <<EOF > slackbot_settings.py
DEBUG = $DEBUG

SE_API_TOKEN = '$SE_API_TOKEN'
SE_API_ENDPOINT = '$SE_API_ENDPOINT'

BOT_ID = '$SLACK_BOT_ID'
API_TOKEN = '$SLACK_API_TOKEN'
ERRORS_TO = '$ERRORS_TO_SLACK'

PLUGINS = [
    'compilebot.plugins',
]
EOF

exec "$@"
