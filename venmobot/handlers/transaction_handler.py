#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import time

import venmobot.tasks
from venmobot.auth import slack_token_authenticated
from venmobot.handlers import BaseHandler
from venmobot.venmo import Venmo


class TransactionHandler(BaseHandler):

    default_return_info = {
        "text": "This is the default return_info, which probably means something " \
                 "went wrong. Please contact the developer with the nature of your " \
                 "attempted request."
    }

    @slack_token_authenticated
    def post(self):
        return_info = self.default_return_info
        action, text = self.process_slack_text(self.arguments.get("text"))
        logging.info("Received '%s' action request from %s" % (action, self.arguments.get("user_name")))
        if not action:
            logging.error("No action received.")
            return_info = {
                "text": "No action was specified for your request. " \
                         "Try \"/venmo help\" to see available options."
             }
        else:
            return_info = self.process_action(action, text)

        self.write(return_info)

    def process_slack_text(self, text):
        split_text = text.split(" ", 1)
        if len(split_text) == 1:
            return split_text[0], None
        return split_text[0], split_text[1]

    def process_action(self, action, text):
        if action == "login":
            logging.info("Generating Venmo OAuth URL...")
            v = Venmo(host_uri=self.base_uri)
            auth_url = v.oauth_authorization_endpoint
            return {
                "text": "Please click <a href='%s'>here</a> in order to authorize " \
                         "Venmobot with Venmo." % auth_url
            }
        elif action == "logout":
            return self.default_return_info
        else:
            logging.error("Could not handle action '%s'." % action)
            return {
                "text": "Sorry, I don't know the action \"%s\". Please check " \
                        "\"/venmo help\" for a list of available actions." % action
            }
