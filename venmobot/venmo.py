#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        self.base_url = sandbox and "https://sandbox-api.venmo.com/v1" or "https://api.venmo.com/v1"
        self.host_uri = host_uri

    @property
    def oauth_authorization_endpoint(self):
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": "%s/oauth" % self.host_uri,
            "scope": " ".join(self.oauth_scopes)
        }
        return "%s/oauth/authorize?%s" % (self.base_url, urllib.urlencode(params))
