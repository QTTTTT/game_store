import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qweqwe'

    @staticmethod
    def init_app(app):
        pass

config = {
    'default': Config,
    'MYSQL_PASSWORD': '11234567',
    'DATABASE_NAME': 'game'
}
