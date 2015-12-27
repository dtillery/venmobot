#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import logging
import os

import tornado.web


def slack_token_authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        request_token = get_slack_request_token(self)
        expected_token = os.environ.get("SLACK_CMD_TOKEN")
        if request_token == expected_token:
            return method(self, *args, **kwargs)
        raise tornado.web.HTTPError(401, 'Could not authenticate Slack request')
    return wrapper

def get_slack_request_token(handler):
    return handler.get_argument("token", None)
