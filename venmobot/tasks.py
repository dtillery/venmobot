#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from celery import Celery

import venmobot.celeryconfig

app = Celery()
app.config_from_object(venmobot.celeryconfig)

@app.task
def pay(request_user_id, target_user, amount, description):
    logging.info("Processing pay request for user %s." % request_user_id)
    logging.info("Target: %s" % target_user)
    logging.info("Amount: %f" % amount)
    logging.info("Description: %s" % description)
