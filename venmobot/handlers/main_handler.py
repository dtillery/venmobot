#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tornado.web import HTTPError, RequestHandler

class MainHandler(RequestHandler):

    def get(self):
        text = "Welcome to Venmobot, the best way to Venmo your teammates on Slack!"
        self.write(text)
