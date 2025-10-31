from flask import Flask
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


import src.views
