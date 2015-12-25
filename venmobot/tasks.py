#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from celery import Celery

import venmobot.celeryconfig

app = Celery()
app.config_from_object(venmobot.celeryconfig)

@app.task
def test():
    logging.info("Test Task Complete!")
