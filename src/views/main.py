# -*- coding: utf-8 -*-
"""
メインルート
Main Routes
"""
from flask import render_template, request, session, redirect, url_for
from src import app


@app.route('/set-language/<lang>')
def set_language(lang):
    """言語を切り替える"""
    supported_languages = app.config.get('SUPPORTED_LANGUAGES', {})
    if lang in supported_languages:
        session['language'] = lang
    # リファラーに戻るか、なければホームへ
    return redirect(request.referrer or url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    """ホームページ - 時間割選択"""
    from src.models import MajorMaster, TimetableModel
    from src.translations.field_values import SEMESTERS, get_semester_name, get_major_name
    from src.translations.ui_text import get_text

    current_lang = session.get('language', app.config.get('DEFAULT_LANGUAGE', 'ja'))

    # POSTリクエストの処理
    if request.method == 'POST':
        semester = request.form.get('semester', type=int)
        major1_id = request.form.get('major1_id', type=int)
        major2_id = request.form.get('major2_id', type=int)

        # バリデーション
        error = None

        # 第一メジャーと第二メジャーが両方選択されているかチェック
        if not major1_id or not major2_id:
            error = get_text('index', 'error_major_required', current_lang)
        # 第一メジャーと第二メジャーが同じでないかチェック
        elif major1_id == major2_id:
            error = get_text('index', 'error_major_same', current_lang)

        # エラーがある場合は、フォームに戻る
        if error:
            return render_template(
                'index.html',
                majors=MajorMaster.query.all(),
                semesters=SEMESTERS,
                selected_semester=semester,
                selected_major1=major1_id,
                selected_major2=major2_id,
                error=error
            )

        # メッセージを作成（バリデーション通過済みなのでmajor1_id, major2_idはNoneではない）
        semester_name = get_semester_name(semester, current_lang) if semester else ''
        # バリデーション通過時点でmajor1_id, major2_idはNoneではないことが保証されている
        assert major1_id is not None and major2_id is not None
        major1_name = get_major_name(major1_id, current_lang)
        major2_name = get_major_name(major2_id, current_lang)

        selection_label = get_text('index', 'selection_label', current_lang)
        semester_label = get_text('index', 'semester', current_lang)
        major1_label = get_text('index', 'major1', current_lang)
        major2_label = get_text('index', 'major2', current_lang)

        message = f'{selection_label}: {semester_label}={semester_name}, {major1_label}={major1_name}, {major2_label}={major2_name}'

        # TODO: 時間割モデルを検索または生成
        # 今は選択された値を表示するだけ
        return render_template(
            'index.html',
            majors=MajorMaster.query.all(),
            semesters=SEMESTERS,
            selected_semester=semester,
            selected_major1=major1_id,
            selected_major2=major2_id,
            message=message
        )
    else:
        # GETリクエストの処理
        return render_template(
            'index.html',
            majors=MajorMaster.query.all(),
            semesters=SEMESTERS
        )
