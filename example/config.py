# -*- coding: UTF-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))
nacl_sk_path = "privateKey.pem"
storage_path = "path/storage"


allowed_file_suffix_list=['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif']

class BaseConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'LearnFlaskTheHardWay.by.JanCUC'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
    BCRYPT_LOG_ROUNDS = 12


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'data-dev.sqlite')


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}