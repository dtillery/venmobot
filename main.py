#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.autoreload
from tornado.options import define, options

from venmobot.handlers.ping_handler import PingHandler
from venmobot.handlers.transaction_handler import TransactionHandler

define("port", default=9001, help="Port for the application to listen on.")
define("debug", default=False, help="Enable debug mode (logging, autoreload, etc...)")
define("slack-cmd-token", default="", help="Token to authenticate the Slash Command from Slack.")


class Application(tornado.web.Application):

    def __init__(self):
        routes = [
            (r"/ping", PingHandler),
            (r"/transactions", TransactionHandler)
        ]

        #TODO: somehow ping celery worker so it comes back up at same time?

        tornado.web.Application.__init__(self, routes)


if __name__ == '__main__':
     # must set format before calling tornado cmdline parsing
    fmt = "%(asctime)s %(levelname)-8.8s %(message)s"
    logging.basicConfig(format=fmt)
    logging.root.setLevel("DEBUG")
    tornado.options.parse_command_line()

    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    if options.debug:
        tornado.autoreload.start()

    logging.info("Starting the application on port %i..." % options.port)
    tornado.ioloop.IOLoop.instance().start()