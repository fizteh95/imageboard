import logging
from logging.handlers import RotatingFileHandler  # SMTPHandler,
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
#from flask_image_alchemy.storages import S3Storage

# from flask_misaka import Misaka

import re
from jinja2 import Markup
  


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
#s3_storage = S3Storage()
login.login_view = 'index'

#app = Flask(__name__)
#app.config.from_object(Config)
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)
#login = LoginManager(app)
#login.login_view = 'index'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    #s3_storage.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')



#     from app.models import ImageClass, User, Board
    
#     users = User.query.all()
#     if len(users) == 0:
#         u = User(username='admin')
#         u.set_password('secret-password')
#         db.session.add(u)
#         db.session.commit()
        
#     boards = Board
#     if len()
    
#     try:
#         file = open('test.txt')  # наличие флаги будет флагом
#     except IOError as e:
#         # загружаем из бд картинки в систему
#         pass
#     else:
#         print('Not first start, okay.')


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


    @app.template_filter('simple_markup')
    def br2br(value):
        result = Markup.escape(value)
        result = result.replace('[i]', Markup('<i>'))
        result = result.replace('[/i]', Markup('</i>'))
        result = result.replace('[b]', Markup('<b>'))
        result = result.replace('[/b]', Markup('</b>'))
        result = result.replace('[u]', Markup('<u>'))
        result = result.replace('[/u]', Markup('</u>'))
        return result

    return app



# if not app.debug:
#     # if app.config['MAIL_SERVER']:
#     #     auth = None
#     #     if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#     #         auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#     #     secure = None
#     #     if app.config['MAIL_USE_TLS']:
#     #         secure = ()
#     #     mail_handler = SMTPHandler(
#     #         mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#     #         fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#     #         toaddrs=app.config['ADMINS'], subject='Microblog Failure',
#     #         credentials=auth, secure=secure)
#     #     mail_handler.setLevel(logging.ERROR)
#     #     app.logger.addHandler(mail_handler)

#     if not os.path.exists('logs'):
#         os.mkdir('logs')
#     file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
#                                        backupCount=10)
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)

#     app.logger.setLevel(logging.INFO)
#     app.logger.info('Microblog startup')

# from app import routes, models, errors






