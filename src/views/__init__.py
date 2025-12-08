# -*- coding: utf-8 -*-
"""
ビューモジュール
Views Module

全てのルートとコンテキストプロセッサーをインポートします。
Imports all routes and context processors.
"""

# コンテキストプロセッサーを登録
from src.views import context_processors

# ルートを登録
from src.views import main
from src.views import errors

__all__ = [
    'context_processors',
    'main',
    'errors',
]
