# -*- coding: utf-8 -*-
"""
UIテキストの翻訳定義
UI Text Translations
"""

# ナビゲーション
NAV = {
    "home": {"ja": "ホーム", "en": "Home"},
    "sql_tool": {"ja": "SQLツール", "en": "SQL Tool"},
}

# 共通
COMMON = {
    "required": {"ja": "必須", "en": "Required"},
    "optional": {"ja": "任意", "en": "Optional"},
    "select_none": {"ja": "選択なし", "en": "None"},
    "submit": {"ja": "送信", "en": "Submit"},
    "execute": {"ja": "実行", "en": "Execute"},
    "cancel": {"ja": "キャンセル", "en": "Cancel"},
    "save": {"ja": "保存", "en": "Save"},
    "delete": {"ja": "削除", "en": "Delete"},
    "edit": {"ja": "編集", "en": "Edit"},
    "create": {"ja": "作成", "en": "Create"},
    "search": {"ja": "検索", "en": "Search"},
    "filter": {"ja": "フィルター", "en": "Filter"},
    "sort": {"ja": "並び替え", "en": "Sort"},
    "count_items": {"ja": "件", "en": "items"},
}

# フッター
FOOTER = {
    "rights_reserved": {"ja": "All rights reserved.", "en": "All rights reserved."},
}

# インデックスページ
INDEX = {
    "title": {"ja": "時間割作成", "en": "Create Timetable"},
    "subtitle": {"ja": "セメスタとメジャーを選択して、あなたの時間割を作成しましょう", "en": "Select your semester and majors to create your timetable"},
    "selection_complete": {"ja": "選択完了", "en": "Selection Complete"},
    "select_timetable": {"ja": "時間割を選択", "en": "Select Timetable"},
    "semester": {"ja": "セメスタ", "en": "Semester"},
    "major1": {"ja": "第一メジャー", "en": "First Major"},
    "major2": {"ja": "第二メジャー", "en": "Second Major"},
    "select_semester": {"ja": "セメスタを選択してください", "en": "Please select a semester"},
    "select_major1": {"ja": "第一メジャーを選択してください", "en": "Please select your first major"},
    "select_major2": {"ja": "第二メジャーを選択してください", "en": "Please select your second major"},
    "major1_help": {"ja": "第一メジャーを選択してください", "en": "Select your first major"},
    "major2_help": {"ja": "第二メジャーを選択してください（第一メジャーと異なるもの）", "en": "Select your second major (different from first major)"},
    "generate_timetable": {"ja": "時間割を生成", "en": "Generate Timetable"},
    "selection_label": {"ja": "選択", "en": "Selection"},
    "error_semester_required": {"ja": "セメスタは必須です。", "en": "Semester is required."},
    "error_major_required": {"ja": "第一メジャーと第二メジャーは必須です。", "en": "First and second majors are required."},
    "error_major_same": {"ja": "第一メジャーと第二メジャーに同じメジャーは選択できません。", "en": "First and second majors must be different."},
    "how_to_use": {"ja": "使い方", "en": "How to Use"},
    "help_semester": {"ja": "セメスタは必須です。2年前期、2年後期、3年前期、3年後期から選択してください。", "en": "Semester is required. Select from 2nd year first semester, 2nd year second semester, 3rd year first semester, or 3rd year second semester."},
    "help_majors": {"ja": "第一メジャーと第二メジャーは必須です。それぞれ異なるメジャーを選択してください。", "en": "First and second majors are required. Select different majors for each."},
    "help_major_types": {"ja": "メジャー:", "en": "Majors:"},
    "help_generate": {"ja": "選択後、「時間割を生成」ボタンをクリックすると、条件に合った時間割が作成されます。", "en": "After selecting, click the 'Generate Timetable' button to create a timetable that matches your criteria."},
}

# SQLツールページ
SQL = {
    "title": {"ja": "SQL クエリツール", "en": "SQL Query Tool"},
    "warning": {"ja": "注意:", "en": "Warning:"},
    "dev_only": {"ja": "このツールは開発環境専用です。本番環境では無効化されます。", "en": "This tool is for development environments only. It will be disabled in production."},
    "enter_query": {"ja": "SQLクエリを入力", "en": "Enter SQL Query"},
    "query": {"ja": "クエリ", "en": "Query"},
    "execute": {"ja": "実行", "en": "Execute"},
    "sample_queries": {"ja": "サンプルクエリ", "en": "Sample Queries"},
    "show_all_tables": {"ja": "全テーブル一覧を表示", "en": "Show All Tables"},
    "show_table_structure": {"ja": "テーブル構造を表示", "en": "Show Table Structure"},
    "get_all_records": {"ja": "全レコードを取得", "en": "Get All Records"},
    "error_occurred": {"ja": "エラーが発生しました", "en": "Error Occurred"},
    "query_success": {"ja": "クエリが正常に実行されました。", "en": "Query executed successfully."},
    "query_results": {"ja": "クエリ結果", "en": "Query Results"},
    "no_results": {"ja": "結果が0件です。", "en": "No results found."},
}

# リザルトページ
RESULT = {
    "title": {"ja": "時間割", "en": "Timetable"},
    "subtitle": {"ja": "選択した条件に基づく時間割", "en": "Timetable based on your selections"},
    "back": {"ja": "戻る", "en": "Back"},
    "selected_conditions": {"ja": "選択した条件", "en": "Selected Conditions"},
    "timetable": {"ja": "時間割表", "en": "Timetable"},
    "generating_message": {"ja": "時間割を生成する機能は現在準備中です。", "en": "Timetable generation feature is currently under development."},
    "period": {"ja": "時限", "en": "Period"},
    "monday": {"ja": "月", "en": "Mon"},
    "tuesday": {"ja": "火", "en": "Tue"},
    "wednesday": {"ja": "水", "en": "Wed"},
    "thursday": {"ja": "木", "en": "Thu"},
    "friday": {"ja": "金", "en": "Fri"},
    "intensive": {"ja": "集中", "en": "Intensive"},
    "intensive_courses": {"ja": "集中講義", "en": "Intensive Courses"},
    "download": {"ja": "ダウンロード", "en": "Download"},
}

# エラーページ
ERROR = {
    "404_title": {"ja": "ページが見つかりません", "en": "Page Not Found"},
    "404_message": {"ja": "お探しのページは存在しません。", "en": "The page you are looking for does not exist."},
    "500_title": {"ja": "サーバーエラー", "en": "Server Error"},
    "500_message": {"ja": "サーバーでエラーが発生しました。", "en": "A server error has occurred."},
    "back_to_home": {"ja": "ホームに戻る", "en": "Back to Home"},
}


def get_text(category: str, key: str, lang: str = 'ja') -> str:
    """
    UIテキストを取得

    Args:
        category: カテゴリ名（NAV, COMMON, INDEX, SQL, ERROR）
        key: テキストキー
        lang: 言語 ('ja' or 'en')

    Returns:
        翻訳されたテキスト
    """
    categories = {
        'nav': NAV,
        'common': COMMON,
        'footer': FOOTER,
        'index': INDEX,
        'result': RESULT,
        'sql': SQL,
        'error': ERROR,
    }

    category_dict = categories.get(category.lower(), {})
    text_dict = category_dict.get(key, {})
    return text_dict.get(lang, key)
