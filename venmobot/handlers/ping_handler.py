#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

from tornado.web import HTTPError, RequestHandler

class PingHandler(RequestHandler):

    def get(self):
        ping_info = {
            "running": True
        }
        self.write(json.dumps(ping_info))
