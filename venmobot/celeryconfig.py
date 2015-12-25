import os

redis_url = os.environ.get("REDIS_URL")

CELERY_IMPORTS = ("venmobot.tasks")

CELERY_RESULT_BACKEND = redis_url

BROKER_URL = redis_url