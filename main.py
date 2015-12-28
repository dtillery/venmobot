#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import urlparse

import psycopg2
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.autoreload
from tornado.options import define, options

from venmobot.handlers.main_handler import MainHandler
from venmobot.handlers.oauth_handler import OauthHandler
from venmobot.handlers.ping_handler import PingHandler
from venmobot.handlers.transaction_handler import TransactionHandler

define("port", default=9001, help="Port for the application to listen on.")
define("debug", default=False, help="Enable debug mode (logging, autoreload, etc...)")


class Application(tornado.web.Application):

    def __init__(self):
        routes = [
            (r"/", MainHandler),
            (r"/ping", PingHandler),
            (r"/transactions", TransactionHandler),
            (r"/oauth", OauthHandler)
        ]

        #TODO: somehow ping celery worker so it comes back up at same time?

        urlparse.uses_netloc.append("postgres")
        env_db_url = os.environ.get("DATABASE_URL")
        db_url = urlparse.urlparse(env_db_url)
        try:
            logging.info("Connecting to DB...")
            self.db_conn = psycopg2.connect(
                database=db_url.path[1:],
                user=db_url.username,
                password=db_url.password,
                host=db_url.hostname,
                port=db_url.port
            )
        except psycopg2.OperationalError as ex:
            logging.error("Problem with connecting to Postgres: %s" % ex)
            sys.exit(1)

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