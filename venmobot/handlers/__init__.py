#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import HTTPError, RequestHandler

class BaseHandler(RequestHandler):

    @property
    def arguments(self):
        if not hasattr(self, "_arguments"):
            self._arguments = {}
            for arg in self.request.arguments:
                self._arguments[arg] = self.get_argument(arg)
        return self._arguments

    @property
    def base_uri(self):
        return "%s//%s" % (self.request.protocol, self.request.host)
