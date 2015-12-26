#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import time

from venmobot.auth import slack_token_authenticated
from venmobot.handlers import BaseHandler
import venmobot.tasks


class TransactionHandler(BaseHandler):

    @slack_token_authenticated
    def post(self):
        logging.info("Transaction Received!")
        logging.info("From User: %s" % self.arguments.get("user_name"))
        logging.info("In channel: %s" % self.arguments.get("channel_name"))
        logging.info("With text: %s" % self.arguments.get("text"))

        venmobot.tasks.test.delay()

        return_info = {
            "text": "Thanks using venmobot, I'll get right on that!",
            "attachments": [
                {
                    "text": "You want to: %s" % self.arguments.get("text")
                }
            ]
        }
        self.write(return_info)
