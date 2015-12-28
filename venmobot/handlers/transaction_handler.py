#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests

from venmobot.auth import slack_token_authenticated
from venmobot.handlers import BaseHandler
from venmobot.venmo import Venmo


class TransactionHandler(BaseHandler):

    default_return_info = {
        "text": "This is the default return_info, which probably means something " \
                 "went wrong. Please contact the developer with the nature of your " \
                 "attempted request."
    }

    help_return_text = """Welcome to Venmobot! Here are the commands I know:
`/venmo help` Access this help menu
`/venmo login` Allow Venmobot access to make payments/charges on your behalf (uses OAuth)
`/venmo logout` Completely remove all information about yourself from Venmobot
"""

    @slack_token_authenticated
    def post(self):
        return_info = self.default_return_info
        action, text = self.process_slack_text(self.arguments.get("text"))
        logging.info("Received '%s' action request from %s" % (action, self.arguments.get("user_name")))
        return_info = self.process_action(action, text)

        self.write(return_info)

    def process_slack_text(self, text):
        split_text = text.split(" ", 1)
        if len(split_text) == 1:
            return split_text[0], None
        return split_text[0], split_text[1]

    def process_action(self, action, text):
        # Return help information
        if action == "help" or not action:
            return {
                "text": self.help_return_text
            }
        # Create Venmo OAuth login URL and send to slack
        elif action == "login":
            slack_id = self.arguments.get("user_id")
            user_name = self.arguments.get("user_name")
            if not slack_id:
                logging.error("No slack_id given for this request: %s" % self.request.arguments)
                return self.default_return_info
            logging.info("Generating Venmo OAuth URL...")
            v = Venmo(host_uri=self.base_uri)
            auth_url = v.get_oauth_authorization_endpoint("|".join([slack_id, user_name]))
            return {
                "text": "Please click <%s|here> in order to authorize " \
                         "Venmobot with Venmo." % auth_url
            }
        # Delete user data from DB by slack_id key
        elif action == "logout":
            logging.info("Removing user %s from database..." % self.arguments.get("user_name"))
            slack_id = self.arguments.get("user_id")
            with self.application.db_conn as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM users WHERE slack_id = %s", (slack_id,))
            logging.info("Deletion succesful")
            return {
                "text": "Your information, including Venmo access tokens, has been succesfully deleted."
            }
        else:
            logging.error("Could not handle action '%s'." % action)
            return {
                "text": "Sorry, I don't know the action \"%s\". Please check " \
                        "\"/venmo help\" for a list of available actions." % action
            }
