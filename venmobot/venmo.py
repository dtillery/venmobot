#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import urllib

import requests

class Venmo(object):

    oauth_scopes = [
        "make_payments"
    ]

    def __init__(self, client_id=None, client_secret=None, sandbox=False, host_uri=None):
        self.client_id = client_id or os.environ.get("VENMO_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("VENMO_CLIENT_SECRET")
        self.base_url = (sandbox or (os.environ.get("VENMO_SANDBOX") == "true")) and "https://sandbox-api.venmo.com/v1" or "https://api.venmo.com/v1"
        self.host_uri = host_uri

    def get_oauth_authorization_endpoint(self, state=None):
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": "%s/oauth" % self.host_uri,
            "scope": " ".join(self.oauth_scopes)
        }
        if state:
            params["state"] = state
        return "%s/oauth/authorize?%s" % (self.base_url, urllib.urlencode(params))
