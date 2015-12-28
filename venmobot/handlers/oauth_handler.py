#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging

import psycopg2

from venmobot.handlers import BaseHandler
from venmobot.venmo import Venmo


class OauthHandler(BaseHandler):

    def get(self):
        if self.arguments.get("error"):
            logging.error("User denied Venmo access.")
            self.write("You cannot use Venmobot unless you allow it to access to your Venmo account.")
            return
        code = self.arguments.get("code")
        if not code:
            # return some sort of error to user
            logging.error("No Code returned for Venmo OAuth: %s" % self.arguments)
            self.write("Looks like something went wrong, please try again later. " \
                       "If the problem persists please contact the Venmobot developers.")
            return

        state = self.arguments.get("state")
        slack_id, user_name = state.split("|")
        if not slack_id or not user_name:
            logging.error("No slack ID and/or Username returned as part of Venmo OAuth.")
            self.write("Looks like something went wrong, please try again later. " \
                       "If the problem persists please contact the Venmobot developers.")
            return

        v = Venmo()
        access_token, refresh_token, expires_in = v.get_access_refresh_tokens(code)

        logging.info("Inserting new user to DB...")
        # insert user into DB based on slack_id
        with self.application.db_conn as conn:
            with conn.cursor() as cursor:
                try:
                    insert_info = {
                        "slack_id": slack_id,
                        "user_name": user_name,
                        "expires_in": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    }
                    cursor.execute("INSERT INTO users (slack_id, user_name, access_token, refresh_token, access_expires) " \
                                   "VALUES (%(slack_id)s, %(user_name)s, %(access_token)s, %(refresh_token)s, %(expires_in)s)",
                                    insert_info)
                except psycopg2.IntegrityError as ex:
                    logging.error("Could not insert User %s: %s" % (insert_info.get("user_name"), ex))
                    self.write("We had a problem logging you in. Did you already " \
                               "log in previously? If so, try using the \"/venmo logout\" " \
                               "command and then logging in again.")
                else:
                    logging.info("Successfully inserted new user %s." % insert_info.get("user_name"))
                    self.write("Cool, we successfully authenticated with Venmo!  You should be able to use Venmobot now.")
                    return