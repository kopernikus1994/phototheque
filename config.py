import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    ENV='development'
    DEBUG=True
    TESTING = True
    SECRET_KEY = 'thisisasecretkey!'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
