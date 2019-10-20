import os
import datetime
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


    # AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID') or 'tratata'
    # AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') or 'tratata'
    # AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME', 'eu-central-1') or 'tratata'
    # S3_BUCKET_NAME = os.environ.get('AWS_REGION_NAME', 'haraka-local') or 'tratata'


    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']
    # POSTS_PER_PAGE = 25
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
