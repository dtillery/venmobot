#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
import requests
import time

from tornado.web import HTTPError, RequestHandler

from venmobot.auth import slack_token_authenticated
import venmobot.tasks


class TransactionHandler(RequestHandler):

    @property
    def arguments(self):
        if not hasattr(self, "_arguments"):
            self._arguments = {}
            for arg in self.request.arguments:
                self._arguments[arg] = self.get_argument(arg)
        return self._arguments

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
                "text": "You want to: %s" % self.arguments.get("text")
            ]
        }
        self.write(json.dumps(return_info))
