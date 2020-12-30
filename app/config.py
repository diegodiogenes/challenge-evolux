# -*- coding: utf-8 -*-

import os


class BaseConfig:
    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = os.urandom(16)


class TestingConfig(BaseConfig):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
