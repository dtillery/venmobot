#!/usr/bin/env python
# -*- coding: utf-8 -*-

from venmobot.handlers import BaseHandler


class MainHandler(BaseHandler):

    def get(self):
        text = "Welcome to Venmobot, the best way to Venmo your teammates on Slack!"
        self.write(text)
