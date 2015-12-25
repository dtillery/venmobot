#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import time

from tornado.web import HTTPError, RequestHandler

from venmobot.auth import slack_token_authenticated


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
        logging.info(self.arguments)

        # 1. Get target phone number from DB
        # If user not in DB, query slack and update
        logging.info("Testing delayed responses")
        time.sleep(3)
        logging.info("3 seconds passed.")
        time.sleep(3)
        logging.info("6 seconds passed.")
        response_url = self.arguments.get("response_url")
        response_data = {
            "response_type": "in_channel",
            "text": "Responding back to %s re:%s!" % (self.arguments.get("user_name"), self.arguments.get("text"))
        }
        logging.info("Sending response to %s" % response_url)
        r = requests.post(response_url, json=response_data)
        logging.info("%i: %s" % (r.status_code, r.content))
