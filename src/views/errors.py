# -*- coding: utf-8 -*-
"""
エラーハンドラー
Error Handlers
"""
from flask import render_template
from src import app


@app.errorhandler(404)
def page_not_found(e):
    """404 ページが見つかりません"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """500 サーバーエラー"""
    return render_template('500.html'), 500
