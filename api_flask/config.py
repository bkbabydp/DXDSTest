# -*- coding: UTF-8 -*-


import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    @staticmethod
    def init_app(app):
        pass


class ConfigDevelopment(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(basedir, 'db/app-development.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    API_VERSION = 'v1'


class ConfigTesting(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(basedir, 'db/app-testing.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    API_VERSION = 'v1'


class ConfigProduction(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(basedir, 'db/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_VERSION = 'v1'


config = {
    'development': ConfigDevelopment,
    'testing': ConfigTesting,
    'production': ConfigProduction,

    'default': ConfigDevelopment
}

del os
