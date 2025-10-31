from flask import render_template
from src import app
from datetime import datetime

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

@app.route('/')
def index():
    return render_template('index.html', message='Hello World!')

@app.route('/test')
def other1():
    return render_template('index.html', message='テストページです！')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
