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
    return redirect(request.referrer or url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    """ホームページ - 時間割選択"""
    from src.models import MajorMaster, TimetableModel
    from src.translations.field_values import SEMESTERS, get_semester_name, get_major_name
    from src.translations.ui_text import get_text

    current_lang = session.get('language', app.config.get('DEFAULT_LANGUAGE', 'ja'))

    if request.method == 'POST':
        semester = request.form.get('semester', type=int)
        major1_id = request.form.get('major1_id', type=int)
        major2_id = request.form.get('major2_id', type=int)

        # バリデーション
        error = None

        # セメスタが選択されているかチェック
        if not semester:
            error = get_text('index', 'error_semester_required', current_lang)
        # 第一メジャーと第二メジャーが両方選択されているかチェック
        elif not major1_id or not major2_id:
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

        # バリデーション通過時点でsemester, major1_id, major2_idはNoneではないことが保証されている
        assert semester is not None and major1_id is not None and major2_id is not None

        semester_name = get_semester_name(semester, current_lang)
        major1_name = get_major_name(major1_id, current_lang)
        major2_name = get_major_name(major2_id, current_lang)

        # セッションに選択内容を保存
        session['semester'] = semester
        session['semester_name'] = semester_name
        session['major1_id'] = major1_id
        session['major1_name'] = major1_name
        session['major2_id'] = major2_id
        session['major2_name'] = major2_name

        # result画面にリダイレクト
        return redirect(url_for('result'))
    else:
        # GETリクエストの処理
        return render_template(
            'index.html',
            majors=MajorMaster.query.all(),
            semesters=SEMESTERS
        )


@app.route('/result')
def result():
    """時間割結果ページ"""
    # セッションから選択内容を取得
    semester = session.get('semester')
    semester_name = session.get('semester_name')
    major1_id = session.get('major1_id')
    major1_name = session.get('major1_name')
    major2_id = session.get('major2_id')
    major2_name = session.get('major2_name')

    # セッションにデータがない場合はトップページにリダイレクト
    if not all([semester, major1_id, major2_id]):
        return redirect(url_for('index'))

    # 現在の言語を取得
    current_lang = session.get('language', app.config.get('DEFAULT_LANGUAGE', 'ja'))

    # 年度情報を取得
    fiscal_year_dict = app.config.get('FISCAL_YEAR', {})
    fiscal_year = fiscal_year_dict.get(current_lang, fiscal_year_dict.get('ja', ''))

    # TODO: 時間割モデルを検索または生成
    # 今は静的な時間割を表示
    return render_template(
        'result.html',
        semester=semester,
        semester_name=semester_name,
        major1_id=major1_id,
        major1_name=major1_name,
        major2_id=major2_id,
        major2_name=major2_name,
        fiscal_year=fiscal_year
    )
