# -*- coding: utf-8 -*-
"""
コンテキストプロセッサー
Context Processors
"""
from flask import session
from src import app
from datetime import datetime


@app.context_processor
def inject_current_year():
    """現在の年をテンプレートで利用可能にする"""
    return {'current_year': datetime.now().year}


@app.context_processor
def inject_language():
    """現在の言語をテンプレートで利用可能にする"""
    from src.translations.ui_text import get_text
    from src.translations.field_values import (
        get_day_name, get_major_name, get_course_category_name,
        get_offering_category_name, get_class_format_name, get_course_type_name,
        get_semester_name
    )

    current_lang = session.get('language', app.config.get('DEFAULT_LANGUAGE', 'ja'))

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

    return {
        'current_language': current_lang,
        'supported_languages': app.config.get('SUPPORTED_LANGUAGES', {}),
        't': t,
        'translate_day': translate_day,
        'translate_major': translate_major,
        'translate_course_category': translate_course_category,
        'translate_offering_category': translate_offering_category,
        'translate_class_format': translate_class_format,
        'translate_course_type': translate_course_type,
        'translate_semester': translate_semester,
    }
