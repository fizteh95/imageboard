import logging
from logging.handlers import RotatingFileHandler  # SMTPHandler,
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager
from config import Config
from flask_misaka import Misaka

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

Misaka(app=app, escape    = True,
                no_images = True,
                wrap      = True,
                autolink  = True,
                no_intra_emphasis = True,
                space_headers     = True)

# login = LoginManager(app)
# login.login_view = 'login'

if not app.debug:
    # if app.config['MAIL_SERVER']:
    #     auth = None
    #     if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #         auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    #     secure = None
    #     if app.config['MAIL_USE_TLS']:
    #         secure = ()
    #     mail_handler = SMTPHandler(
    #         mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #         fromaddr='no-reply@' + app.config['MAIL_SERVER'],
    #         toaddrs=app.config['ADMINS'], subject='Microblog Failure',
    #         credentials=auth, secure=secure)
    #     mail_handler.setLevel(logging.ERROR)
    #     app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors


import re
from jinja2 import Markup


_reply_re = re.compile(r'(>>\d+)')


@app.template_filter('regex_replace')
def nl2br(value):
    result = ''
    arr = _reply_re.split(value)
    for i in range(len(arr)):
        if i % 2 == 0:
            result += arr[i]
        else:
            result += Markup('<a href="#post_num_' + str(arr[i]).split('>>')[-1] + '" class="inline_reply" onmouseenter="ref_over(event, this)" onmouseleave="ref_out()">' + arr[i] + '</a>')
    return result
