# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
MIO_HOST = os.environ.get('MIO_HOST', '127.0.0.1')
MIO_PORT = int(os.environ.get('MIO_PORT', 5000))
MIO_SITE_HOST = os.environ.get('MIO_SITE_HOST', MIO_HOST)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mio'  # 默认秘钥
    SESSION_TYPE = 'filesystem'
    # 邮件系统设置相关
    MIO_MAIL = False
    MIO_SEND_MAIL = False
    MAIL_SUBJECT_PREFIX = os.environ.get('MIO_MAIL_SUBJECT_PREFIX', '[Mio System]')  # 默认邮件标题前缀
    MAIL_SENDER = os.environ.get('MIO_MAIL_SERVER', 'Mio System Administrator <admin@example.com>')  # 默认发件人
    MAIL_SERVER = os.environ.get('MIO_MAIL_SERVER', 'localhost')
    MAIL_PORT = os.environ.get('MIO_MAIL_PORT', 25)
    MAIL_USE_TLS = os.environ.get('MIO_MAIL_USE_TLS', False)
    MAIL_USERNAME = os.environ.get('MIO_MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MIO_MAIL_PASSWORD', '')
    # 是否使用MONGODB
    MONGODB_ENABLE = os.environ.get('MIO_MONGODB_ENABLE', False)
    # 是否使用RabbitMQ
    RABBITMQ_ENABLE = os.environ.get('MIO_RABBITMQ_ENABLE', False)
    # 是否使用Redis
    REDIS_ENABLE = os.environ.get('MIO_REDIS_ENABLE', False)
    # 是否使用ssdb
    SSDB_ENABLE = os.environ.get('MIO_SSDB_ENABLE', False)
    # 是否使用关系型数据库 支持sqlite, mysql, pgsql
    RMDB_SYS_ENABLE = os.environ.get('MIO_RMDB_SYS_ENABLE', False)
    # 是否使用CORS
    CORS_ENABLE = os.environ.get('MIO_CORS_ENABLE', False)
    CORS_URI = os.environ.get('MIO_CORS_URI', {r"/*": {"origins": "*"}})
    # 定时任务相关
    CRON_ENABLE = os.environ.get('MIO_CRON_ENABLE', False)
    # at: 分 时 日 月 周
    CRON_SETTING = [
        {
            'name': 'RabbitMQ Sender',
            'file': 'cron.Mq',
            'class': 'Sender',
            'at': '* * * * *'
        }
    ]

    @staticmethod
    def init_app(app):
        app.jinja_env.trim_blocks = True
        app.jinja_env.lstrip_blocks = True


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'db_name',
        'host': 'localhost',
        'username': 'username',
        'password': 'password',
        'connect': False
    }
    RABBITMQ_SETTING = {
        'default': {
            'host': 'localhost',
            'port': '5672',
            'vhost': 'vhost',
            'user': 'username',
            'pass': 'password'
        }
    }
    SSDB_SETTINGS = {
        'host': 'localhost',
        'port': 8888,
        'auth': None
    }
    REDIS_URL = 'redis://10.0.0.82:6379/0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://username:password@hostname/database'


class TestingConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'db_name',
        'host': 'localhost',
        'username': 'username',
        'password': 'password',
        'connect': False
    }
    RABBITMQ_SETTING = {
        'default': {
            'host': 'localhost',
            'port': '5672',
            'vhost': 'vhost',
            'user': 'username',
            'pass': 'password'
        }
    }
    SSDB_SETTINGS = {
        'host': 'localhost',
        'port': 8888,
        'auth': None
    }
    REDIS_URL = 'redis://localhost:6379/0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'postgresql://username:password@hostname/database'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        'db': 'db_name',
        'host': 'localhost',
        'username': 'username',
        'password': 'password',
        'connect': False
    }
    RABBITMQ_SETTING = {
        'default': {
            'host': 'localhost',
            'port': '5672',
            'vhost': 'vhost',
            'user': 'username',
            'pass': 'password'
        }
    }
    SSDB_SETTINGS = {
        'host': 'localhost',
        'port': 8888,
        'auth': None
    }
    REDIS_URL = 'redis://10.0.0.82:6379/0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://username:password@hostname/database'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
