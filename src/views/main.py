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
    from src.models import MajorMaster
    from src.translations.field_values import SEMESTERS

    if request.method == 'POST':
        semester = request.form.get('semester', type=int)
        major1_id = request.form.get('major1_id', type=int)
        major2_id = request.form.get('major2_id', type=int)

        assert semester is not None and major1_id is not None and major2_id is not None

        # result画面にリダイレクト（クエリパラメータ付き）
        return redirect(url_for('result',
                                semester=semester,
                                major1_id=major1_id,
                                major2_id=major2_id))
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
    from src.translations.field_values import get_semester_name, get_major_name

    # 現在の言語を取得
    current_lang = session.get('language', app.config.get('DEFAULT_LANGUAGE', 'ja'))

    # クエリパラメータから選択内容を取得
    semester = request.args.get('semester', type=int)
    major1_id = request.args.get('major1_id', type=int)
    major2_id = request.args.get('major2_id', type=int)

    # データがない場合はホーム画面にリダイレクト
    if not all([semester, major1_id, major2_id]):
        return redirect(url_for('index'))

    # 型チェック後、semester, major1_id, major2_idはNoneではないことが保証されている
    assert semester is not None and major1_id is not None and major2_id is not None

    # 名前を取得
    semester_name = get_semester_name(semester, current_lang)
    major1_name = get_major_name(major1_id, current_lang)
    major2_name = get_major_name(major2_id, current_lang)

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
