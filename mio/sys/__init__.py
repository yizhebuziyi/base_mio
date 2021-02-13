# -*- coding: utf-8 -*-
import os
import sys
import yaml
import codecs
import logging
from flask import Flask, blueprints
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_babel import Babel
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_mongoengine import MongoEngine
from flask_redis import FlaskRedis
from flask_mail import Mail
# from numba import jit
from typing import Tuple, Optional, List
from mio.util.Helper import in_dict, is_enable
from mio.util.Logs import LogHandler, LoggerType
from mio.sys.wsgi import MIO_SYSTEM_VERSION

mail: Mail = Mail()
crypt: Bcrypt = Bcrypt()
db: MongoEngine = MongoEngine()
redis_db: FlaskRedis = FlaskRedis()
csrf: CSRFProtect = CSRFProtect()
login_manager: LoginManager = LoginManager()


# @jit(nogil=True, forceobj=True)
def create_app(config_name: str, root_path: Optional[str] = None, config_clz: Optional[str] = None,
               logger_type: LoggerType = LoggerType.CONSOLE,
               log_level: int = logging.DEBUG) -> Tuple[Flask, List[tuple]]:
    console = LogHandler('InitApp', logger_type=logger_type, log_level=log_level)
    console.info(u'Initializing the system......profile: {}'.format(config_name))
    config_clz: str = 'config' if not isinstance(config_clz, str) else config_clz.strip()
    config_path: str = os.path.join(root_path, config_clz.replace('.', '/'))
    clazz = __import__(config_clz, globals(), fromlist=['config'])
    config: dict = getattr(clazz, 'config')
    yaml_file: str = os.path.join(config_path, 'config.yaml')
    if not os.path.isfile(yaml_file):
        console.error(u'config.yaml not found!')
        sys.exit(0)
    config_yaml: dict = yaml.load(codecs.open(yaml_file, 'r', 'utf-8'), Loader=yaml.FullLoader)
    if not in_dict(config_yaml, 'config'):
        console.error(u'config.yaml format error!')
        sys.exit(0)
    base_config: dict = config_yaml['config']
    static_folder: str = '{root_path}/web/static' if not in_dict(base_config, 'static_folder') \
        else base_config['static_folder']
    static_folder = static_folder.replace('{root_path}', root_path)
    static_folder = os.path.abspath(static_folder)
    if not os.path.isdir(static_folder):
        console.error(u'Static file path not found!')
        sys.exit(0)
    template_folder: str = '{root_path}/web/template' if not in_dict(base_config, 'template_folder') \
        else base_config['template_folder']
    template_folder = template_folder.replace('{root_path}', root_path)
    template_folder = os.path.abspath(template_folder)
    if not os.path.isdir(template_folder):
        console.error(u'Template path not found!')
        sys.exit(0)
    config_name: str = 'default' if not isinstance(config_name, str) else config_name
    config_name = config_name.lower()
    if not in_dict(config, config_name):
        console.error(u'Config invalid!')
        sys.exit(0)
    app: Flask = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    babel: Babel = Babel(app)
    if in_dict(base_config, 'csrf'):
        if is_enable(base_config['csrf'], 'enable'):
            csrf.init_app(app)
    if in_dict(base_config, 'login_manager'):
        if is_enable(base_config['login_manager'], 'enable'):
            login_manager_config: dict = base_config['login_manager']
            login_manager.session_protection = 'strong' if not in_dict(login_manager_config, 'session_protection') \
                else login_manager_config['session_protection']
            login_manager.login_view = 'main.login' if not in_dict(login_manager_config, 'login_view') else \
                login_manager_config['login_view']
            if in_dict(login_manager_config, 'login_message'):
                login_manager.login_message = login_manager_config['login_message']
            if in_dict(login_manager_config, 'login_message_category'):
                login_manager.login_message_category = login_manager_config['login_message_category']
            login_manager.init_app(app)
    if is_enable(app.config, 'MIO_MAIL'):
        mail.init_app(app)
    if is_enable(app.config, 'MONGODB_ENABLE'):
        db.init_app(app)
    if is_enable(app.config, 'REDIS_ENABLE'):
        redis_db.init_app(app)
    if is_enable(app.config, 'CORS_ENABLE'):
        if not in_dict(app.config, 'CORS_URI'):
            console.error(u'CORS_URI not define.')
            sys.exit(0)
        CORS(app, resources=app.config['CORS_URI'])
    blueprints_config: List[dict] = config_yaml['blueprint'] if in_dict(config_yaml, 'blueprint') else []
    for blueprint in blueprints_config:
        key: str = list(blueprint.keys())[0]
        clazz = __import__(blueprint[key]['class'], globals(), fromlist=[key])
        bp: blueprints.Blueprint = getattr(clazz, key)
        if in_dict(blueprint[key], 'url_prefix'):
            app.register_blueprint(bp, url_prefix=blueprint[key]['url_prefix'])
        else:
            app.register_blueprint(bp)
    wss: List[tuple] = []
    websocket_config: List[dict] = config_yaml['websocket'] if in_dict(config_yaml, 'websocket') else []
    for websocket in websocket_config:
        key: str = list(websocket.keys())[0]
        clazz = __import__(websocket[key]['class'], globals(), fromlist=[key])
        ws = getattr(clazz, key)
        if not in_dict(websocket[key], 'path'):
            console.error('Path must be set in config.yaml.')
            sys.exit(0)
        wss.append((websocket[key]['path'], ws))
    return app, wss
