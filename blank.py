'''
Везде, где используются конфиги, надо заменить app на current_app, импортировав его из flask

from flask import current_app

if current_app.config['SUPER_SECRET_KEY']:
    pass

'''
