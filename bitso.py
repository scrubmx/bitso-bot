#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
import requests as http
from twilio.rest import TwilioRestClient

try:
   TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
   TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
except KeyError as e:
   print "Please set the environment variable {key}".format(key=e)
   sys.exit(1)

THRESHOLD_PRICE = 13000

def send_notification():
    twilio = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    body = "Price has fallen below your threshold - {amount}".format(
        amount=THRESHOLD_PRICE
        )

    message = twilio.messages.create(body=body,
        to="+525517983239",
        from_="+12569608656")

    print(message.sid)

def main():
    response = http.get('https://api.bitso.com/v2/ticker').json()

    if (float(response['last']) < float(THRESHOLD_PRICE)):
        send_notification()
        sys.exit(0)

if __name__ == '__main__':
    main()
