import os

redis_url = os.environ.get("REDIS_URL")

CELERY_IMPORTS = ("venmobot.tasks")
BROKER_URL = redis_url
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = redis_url
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5