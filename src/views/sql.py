# -*- coding: utf-8 -*-
"""
SQL開発ツールルート
SQL Development Tool Routes
"""
from flask import render_template, request, session
from sqlalchemy import text
from src import app, db


@app.route('/sql', methods=['GET', 'POST'])
def sql():
    """SQL クエリ実行ツール（開発用）"""
    from src.translations.ui_text import get_text

    # セキュリティ: DEBUG モードでのみ有効
    if not app.config.get('DEBUG'):
        return render_template('404.html'), 404

    current_lang = session.get('language', app.config.get('DEFAULT_LANGUAGE', 'ja'))
    results = None
    error = None
    query = ''
    columns = []

    if request.method == 'POST':
        query = request.form.get('query', '')

        if query.strip():
            try:
                # クエリを実行
                result = db.session.execute(text(query))

                # SELECT クエリの場合、結果を取得
                if query.strip().upper().startswith('SELECT'):
                    rows = result.fetchall()
                    if rows:
                        # カラム名を取得
                        columns = list(result.keys())
                        # 結果を辞書のリストに変換
                        results = [dict(zip(columns, row)) for row in rows]
                    else:
                        results = []
                else:
                    # INSERT, UPDATE, DELETE などの場合
                    db.session.commit()
                    results = get_text('sql', 'query_success', current_lang)

            except Exception as e:
                error = str(e)
                db.session.rollback()

    return render_template(
        'sql.html',
        query=query,
        results=results,
        columns=columns,
        error=error
    )
