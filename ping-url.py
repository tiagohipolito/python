#!/usr/bin/env python

import datetime
import requests, json

URLS_LIST_FILE="/usr/local/etc/urls"
LOG="/var/run"
LOG_FILE="/var/log/ping-url.log"
LOG_MAIL="/var/run/log_mail"

SLACK_URL = 'https://hooks.slack.com/services/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'



NOW_STRING=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_slack_message(message, icon):
    payload = {
        'channel':'@talves',
        'username':'vm90-ping-url-python',
        'text':message,
        'icon_emoji': icon
    }
    r = requests.post(SLACK_URL, json.dumps(payload))
    print r

def load_urls():
    url_list = open(URLS_LIST_FILE).readlines()



send_slack_message('teste', ':white_check_mark:')
