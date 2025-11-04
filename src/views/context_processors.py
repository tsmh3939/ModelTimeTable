# -*- coding: utf-8 -*-
"""
コンテキストプロセッサー
Context Processors
"""
from flask import request, redirect
from src import app
from datetime import datetime
from urllib.parse import urlencode

# クエリパラメータの優先順序
QUERY_PARAM_ORDER = ['lang', 'theme']


def order_query_params(params: dict, add_defaults: bool = False, default_lang: str | None = None, default_theme: str | None = None):
    """
    クエリパラメータを指定された順序に並べる

    Args:
        params: パラメータの辞書
        add_defaults: Trueの場合、デフォルト値を追加
        default_lang: langのデフォルト値（Noneの場合はapp.configから取得）
        default_theme: themeのデフォルト値（Noneの場合はapp.configから取得）

    Returns:
        順序付けられたパラメータの辞書
    """
    ordered = {}

    # デフォルト値を追加する場合
    if add_defaults:
        # デフォルト値を取得
        if default_lang is None:
            default_lang = app.config.get('DEFAULT_LANGUAGE', 'ja')
        if default_theme is None:
            default_theme = app.config.get('DEFAULT_THEME_NAME', 'light')

        # paramsをコピーして、不足しているパラメータにデフォルト値を設定
        params = dict(params)
        if 'lang' not in params:
            params['lang'] = default_lang
        if 'theme' not in params:
            params['theme'] = default_theme

    # 優先順序のパラメータを先に追加
    for key in QUERY_PARAM_ORDER:
        if key in params:
            ordered[key] = params[key]

    # 残りのパラメータを追加
    for key, value in params.items():
        if key not in QUERY_PARAM_ORDER:
            ordered[key] = value

    return ordered


@app.before_request
def ensure_lang_and_theme():
    """
    全てのリクエストで言語とテーマのクエリパラメータを確認
    ない場合はデフォルト値を追加してリダイレクト
    """
    # 静的ファイルへのリクエストは無視
    if request.path.startswith('/static/'):
        return None

    # POSTリクエストの場合はリダイレクトしない（フォームデータが失われるため）
    if request.method == 'POST':
        return None

    # langまたはthemeがない場合は追加
    needs_redirect = False

    if 'lang' not in request.args:
        needs_redirect = True

    if 'theme' not in request.args:
        needs_redirect = True

    # リダイレクトが必要な場合
    if needs_redirect:
        # 順序を保証し、デフォルト値を追加
        ordered_args = order_query_params(dict(request.args), add_defaults=True)
        query_string = urlencode(ordered_args)
        return redirect(f"{request.path}?{query_string}")

    return None


@app.context_processor
def inject_current_year():
    """現在の年をテンプレートで利用可能にする"""
    return {'current_year': datetime.now().year}


@app.context_processor
def inject_language():
    """現在の言語とテーマをテンプレートで利用可能にする"""
    from src.translations.ui_text import get_text
    from src.translations.field_values import (
        get_day_name, get_major_name, get_course_category_name,
        get_offering_category_name, get_class_format_name, get_course_type_name,
        get_semester_name
    )
    from flask import url_for as flask_url_for
    from urllib.parse import urlencode

    # クエリパラメータから言語を取得（なければデフォルト）
    current_lang = request.args.get('lang', app.config.get('DEFAULT_LANGUAGE', 'ja'))
    assert isinstance(current_lang, str)

    # クエリパラメータからテーマを取得（なければデフォルト）
    current_theme = request.args.get('theme', app.config.get('DEFAULT_THEME_NAME', 'light'))

    def t(category, key):
        """翻訳テキストを取得"""
        return get_text(category, key, current_lang)

    def translate_day(day_id, short=False):
        """曜日を翻訳"""
        return get_day_name(day_id, current_lang, short)

    def translate_major(major_id):
        """メジャーを翻訳"""
        return get_major_name(major_id, current_lang)

    def translate_course_category(category_id):
        """履修区分を翻訳"""
        return get_course_category_name(category_id, current_lang)

    def translate_offering_category(category_id):
        """開講区分を翻訳"""
        return get_offering_category_name(category_id, current_lang)

    def translate_class_format(format_id):
        """授業形態を翻訳"""
        return get_class_format_name(format_id, current_lang)

    def translate_course_type(type_id):
        """授業種別を翻訳"""
        return get_course_type_name(type_id, current_lang)

    def translate_semester(semester_id):
        """セメスタを翻訳"""
        return get_semester_name(semester_id, current_lang)

    def url_for(endpoint, **values):
        """
        url_forのラッパー関数
        現在の言語とテーマを自動的にクエリパラメータに追加
        順序を保証
        """
        # 順序を保証し、デフォルト値（現在のlangとtheme）を追加
        ordered_values = order_query_params(values, add_defaults=True, default_lang=current_lang, default_theme=current_theme)
        return flask_url_for(endpoint, **ordered_values)

    def update_query_params(**new_params):
        """
        現在のURLのクエリパラメータを更新
        新しいパラメータで上書き、それ以外は保持
        順序を保証
        """
        # 現在のクエリパラメータをコピーして更新
        all_params = dict(request.args)
        all_params.update(new_params)

        # 順序を保証し、デフォルト値を追加（念のため）
        ordered_params = order_query_params(all_params, add_defaults=True, default_lang=current_lang, default_theme=current_theme)

        # クエリ文字列を生成
        query_string = urlencode(ordered_params)
        # 現在のパスと組み合わせる
        return f"{request.path}?{query_string}"

    return {
        'current_language': current_lang,
        'current_theme': current_theme,
        'supported_languages': app.config.get('SUPPORTED_LANGUAGES', {}),
        't': t,
        'translate_day': translate_day,
        'translate_major': translate_major,
        'translate_course_category': translate_course_category,
        'translate_offering_category': translate_offering_category,
        'translate_class_format': translate_class_format,
        'translate_course_type': translate_course_type,
        'translate_semester': translate_semester,
        'url_for': url_for,
        'update_query_params': update_query_params,
    }
