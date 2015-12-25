import os

redis_url = os.environ.get("REDIS_URL")

CELERY_RESULT_BACKEND = "redis"
REDIS_URL = redis_url

BROKER_BACKEND = "redis"
BROKER_URL = redis_url