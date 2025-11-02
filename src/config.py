import os

APP_NAME = "ModelTimeTable"
DEFAULT_THEME_NAME = "light"
DEBUG = True

# データベース設定
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
