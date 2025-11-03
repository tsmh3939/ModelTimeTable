from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


dir_name = os.path.dirname(__file__)
template_folder = os.path.join(dir_name, 'templates')
static_folder = os.path.join(dir_name, 'static')

app = Flask(
    __name__,
    template_folder=template_folder,
    static_folder=static_folder
)
app.config.from_object('src.config')


# データベースのインスタンスを作成
db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()

basedir = os.path.abspath(os.path.dirname(__file__))
db_name = os.environ.get("FLASK_DB_NAME", "modeltimetable.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースの初期化
db.init_app(app)
migrate.init_app(app, db)


import src.views
import src.models

