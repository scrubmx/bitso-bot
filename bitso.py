#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
import datetime
import requests as http
from twilio.rest import TwilioRestClient

try:
    TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
except KeyError as e:
    print "Please set the environment variable {key}".format(key=e)
    sys.exit(1)

THRESHOLD_PRICE = 13000


def current_timestamp():
    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def send_notification():
    twilio = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    body = "Price has fallen below your threshold - {amount}".format(
        amount=THRESHOLD_PRICE)

    message = twilio.messages.create(body=body,
        to="+525517983239",
        from_="+12569608656")

    store_notification(message.sid, body, amount)


def store_notification(id, body, amount):
    connection = sqlite3.connect('notifications.sqlite3')

    with connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO notifications VALUES(?, ?, ?, ?)",
            id, body, amount, current_timestamp())


def should_send_notification():
    connection = sqlite3.connect('notifications.sqlite3')

    with connection:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER NOT NULL,
                body CHAR(255),
                price INTEGER,
                created_at TIMESTAMP DEFAULT NULL);""")

        cursor.execute("SELECT * FROM notifications WHERE created_at >= ? LIMIT 1;",
            current_timestamp())

        row = cursor.fetchone()

        return row == None


def main():
    response = http.get('https://api.bitso.com/v2/ticker').json()

    if (float(response['last']) < float(THRESHOLD_PRICE)):
        if (should_send_notification()):
            send_notification()

if __name__ == '__main__':
    main()
