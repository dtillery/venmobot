#!/usr/bin/env python
# -*- coding: utf-8 -*-

from venmobot.handlers import BaseHandler


class PingHandler(BaseHandler):

    def get(self):
        ping_info = {
            "running": True
        }
        self.write(ping_info)
