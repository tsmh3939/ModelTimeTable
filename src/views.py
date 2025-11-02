from flask import render_template, request, session, redirect, url_for
from src import app, db
from datetime import datetime
from sqlalchemy import text

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

@app.context_processor
def inject_language():
    """現在の言語をテンプレートで利用可能にする"""
    current_lang = session.get('language', app.config.get('DEFAULT_LANGUAGE', 'ja'))
    return {
        'current_language': current_lang,
        'supported_languages': app.config.get('SUPPORTED_LANGUAGES', {})
    }

@app.route('/set-language/<lang>')
def set_language(lang):
    """言語を切り替える"""
    supported_languages = app.config.get('SUPPORTED_LANGUAGES', {})
    if lang in supported_languages:
        session['language'] = lang
    # リファラーに戻るか、なければホームへ
    return redirect(request.referrer or url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', message='Hello World!')

@app.route('/test')
def test():
    return render_template('index.html', message='テストページです！')

@app.route('/sql', methods=['GET', 'POST'])
def sql():
    """SQL クエリ実行ツール（開発用）"""
    # セキュリティ: DEBUG モードでのみ有効
    if not app.config.get('DEBUG'):
        return render_template('404.html'), 404

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
                    results = "クエリが正常に実行されました。"

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
