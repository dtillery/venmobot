#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import urlparse

from celery import Celery, Task
import psycopg2
from slackclient import SlackClient

import venmobot.celeryconfig

app = Celery()
app.config_from_object(venmobot.celeryconfig)

class DatabaseTask(Task):
    abstract = True
    _db = None

    def __init__(self, *args, **kwargs):
        urlparse.uses_netloc.append("postgres")
        env_db_url = os.environ.get("DATABASE_URL")
        db_url = urlparse.urlparse(env_db_url)
        try:
            logging.info("Connecting to DB...")
            self._db = psycopg2.connect(
                database=db_url.path[1:],
                user=db_url.username,
                password=db_url.password,
                host=db_url.hostname,
                port=db_url.port
            )
        except psycopg2.OperationalError as ex:
            logging.error("Problem with connecting to Postgres: %s" % ex)
        super(DatabaseTask, self).__init__(*args, **kwargs)

    @property
    def db_conn(self):
        if self._db is None:
            raise Exception("Not connected to Postgress DB: %s" % ex)
        return self._db

@app.task(base=DatabaseTask)
def pay(request_user_id, target_user, amount, description):
    logging.info("Processing pay request for user %s." % request_user_id)
    # get requesting user's credentials from DB
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    if not slack_token:
        logging.error("SLACK_BOT_TOKEN not found in environment.")
        # error response to user
        return
    slack_client = SlackClient(slack_token)
    # get entire users list and fine target user/phone
    response = json.loads(slack_client.api_call("users.list"))
    if not response.get("ok"):
        logging.error("Problem with getting Slack users list: %s" % response.get("error"))
        # error response to user
        return
    users = {user.get("name"): user.get("profile", {}).get("phone") for user in response.get("members", [])}
    # logging.info(users)
    target_user = target_user.replace("@", "")
    if target_user not in users:
        logging.error("Could not find profile for user %s in Slack" % target_user)
        # error response to user
        return
    target_phone = users.get(target_user)
    if not target_phone:
        logging.error("User %s has no phone number in Slack" % target_user)
        # error response to user
        return

    # pay user via Venmo

