#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from venmobot.handlers import BaseHandler


class OauthHandler(BaseHandler):

    def get(self):
        if self.arguments.get("error"):
            self.write("You cannot use Venmobot unless you allow it to access to your Venmo account.")
        code = self.arguments.get("code")
        if not code:
            # return some sort of error to user
            pass
        logging.info("OAuth Code is %s" % code)
