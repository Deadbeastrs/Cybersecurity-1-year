import os
import logging
from flask import Flask
from .socket import socketio
from .tm import tm_bp
from .rm import rm_bp, authorization, require_oauth
from .oauth2 import configOauth

#Testing
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def create_app(config=None):
    app = Flask(__name__)

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)

    setup_app(app)
    return app

def setup_app(app):
    #Configure Flask Server
    configOauth(app,authorization,require_oauth)
    # TM/MM endpoints
    app.register_blueprint(tm_bp, url_prefix='')
    # RM endpoints
    app.register_blueprint(rm_bp, url_prefix='')
    socketio.init_app(app,async_handlers=True,ping_interval=120)
