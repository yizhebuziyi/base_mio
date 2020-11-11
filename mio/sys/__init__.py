# -*- coding: utf-8 -*-
import os
import sys
import yaml
import codecs
import logging
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from mio.util.Logs import LogHandler
from mio.sys.wsgi import MIO_SYSTEM_VERSION

mail = None
send_mail = None
db = None
crypt = Bcrypt()
ssdb = None
redis_db = None
rmdb = None
csrf = CSRFProtect()
login_manager = LoginManager()
blueprint_config = []


def create_app(config_name, root_path=None, config_clz=None, log_file=None, log_level=logging.DEBUG):
    console = LogHandler('InitApp', log_file=log_file, log_level=log_level)
    console.info(u'Initializing the system......profile: {}'.format(config_name))
    config_clz = 'config' if config_clz is None or not isinstance(config_clz, str) else config_clz.strip()
    config_path = os.path.join(root_path, config_clz.replace('.', '/'))  # 包名转换为路径
    is_default_config = False
    clz_init_file = os.path.join(config_path, '__init__.py')
    try:
        config_yaml = {}
        clazz = __import__(config_clz, globals(), locals(), ['config'])
        config = getattr(clazz, 'config')
        yaml_file = os.path.join(config_path, 'config.yaml')
        if os.path.exists(yaml_file) and os.path.isfile(yaml_file):
            with codecs.open(yaml_file, 'r', 'utf-8') as f:
                config_yaml = yaml.load(f, Loader=yaml.FullLoader)
        # 基础配置
        base_config = config_yaml['config'] if 'config' in config_yaml else {}
        # 登录管理
        login_manager_config = base_config['login_manager'] if 'login_manager' in base_config else {}
        login_manager.session_protection = login_manager_config['session_protection'] if \
            'session_protection' in login_manager_config else 'strong'
        login_manager.login_view = login_manager_config['login_view'] if \
            'login_view' in login_manager_config else 'main.login'
        if 'login_message' in login_manager_config:
            login_manager.login_message = login_manager_config['login_message']
        if 'login_message_category' in login_manager_config:
            login_manager.login_message_category = login_manager_config['login_message_category']
        # 读取静态文件夹配置
        static_folder = base_config['static_folder'] if \
            'static_folder' in base_config else '{root_path}/web/static'
        static_folder = static_folder.replace('{root_path}', root_path)
        static_folder = os.path.abspath(static_folder)
        if not os.path.exists(static_folder) or not os.path.isdir(static_folder):
            os.makedirs(static_folder)
            console.error(u'Static file path not found! Created!')
        template_folder = base_config['template_folder'] if \
            'template_folder' in base_config else '{root_path}/web/template'
        template_folder = template_folder.replace('{root_path}', root_path)
        template_folder = os.path.abspath(template_folder)
        if not os.path.exists(template_folder) or not os.path.isdir(template_folder):
            os.makedirs(template_folder)
            console.info(u'Template path not found! Created!')
        # Flask 基础配置
        config_name = 'default' if config_name is None or not isinstance(config_name, str) else config_name
        config_name = config_name.lower()
        if config_name not in list(config.keys()):
            console.error(u'Config invalid.')
            sys.exit()
        app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)
        babel = Babel(app)
        if app.config['MIO_MAIL']:
            from flask_mail import Mail
            global mail
            mail = Mail()
            mail.init_app(app)
        if app.config['MIO_SEND_MAIL']:
            from flask_sendmail import Mail as SendMail
            global send_mail
            send_mail = SendMail()
            send_mail.init_app(app)
        if 'csrf' in base_config and 'enable' in base_config['csrf'] and base_config['csrf']['enable']:
            csrf.init_app(app)
        if app.config['MONGODB_ENABLE']:
            from flask_mongoengine import MongoEngine
            global db
            db = MongoEngine()
            db.init_app(app)
        if app.config['REDIS_ENABLE']:
            from flask_redis import FlaskRedis
            global redis_db
            redis_db = FlaskRedis()
            redis_db.init_app(app)
        if app.config['CORS_ENABLE']:
            from flask_cors import CORS
            CORS(app, resources=app.config['CORS_URI'])
        if app.config['RMDB_SYS_ENABLE']:
            from flask_sqlalchemy import SQLAlchemy
            global rmdb
            rmdb = SQLAlchemy()
            rmdb.init_app(app)
        if 'SSDB_ENABLE' in app.config and app.config['SSDB_ENABLE']:
            if 'SSDB_SETTINGS' in app.config:
                ssdb_setting = app.config['SSDB_SETTINGS']
                if 'host' in ssdb_setting and 'port' in ssdb_setting and 'auth' in ssdb_setting:
                    from mio.util.SSDB import SSDB
                    global ssdb
                    ssdb = SSDB(ssdb_setting['host'], int(ssdb_setting['port']))
                    if ssdb_setting['auth'] is not None:
                        ssdb.request('auth', ssdb_setting['auth'])
        if 'login_manager' in base_config and 'enable' in base_config['login_manager'] \
                and base_config['login_manager']['enable']:
            login_manager.init_app(app)
        # 蓝本配置
        blueprints_config = config_yaml['blueprint'] if 'blueprint' in config_yaml else []
        for blueprint in blueprints_config:
            key = list(blueprint.keys())[0]
            clazz = __import__(blueprint[key]['class'], globals(), locals(), [key])
            bp = getattr(clazz, key)
            if 'url_prefix' in blueprint[key]:
                app.register_blueprint(bp, url_prefix=blueprint[key]['url_prefix'])
            else:
                app.register_blueprint(bp)
        # ws配置
        wss = []
        websocket_config = config_yaml['websocket'] if 'websocket' in config_yaml else []
        for websocket in websocket_config:
            key = list(websocket.keys())[0]
            clazz = __import__(websocket[key]['class'], globals(), locals(), [key])
            ws = getattr(clazz, key)
            if 'path' not in websocket[key]:
                console.error('Path must be set in config.yaml.')
                exit(0)
            wss.append((websocket[key]['path'], ws))
        return app, wss
    except Exception as e:
        console.error(u'Initializing the system has error：{}'.format(str(e)))
        sys.exit()
