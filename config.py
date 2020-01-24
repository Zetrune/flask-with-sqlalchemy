import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ['SECRET_KEY']
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
    CELERY_BROKER_URL = os.environ['REDIS_URL']
