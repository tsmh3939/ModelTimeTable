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
    "title": {"ja": "モデル時間割", "en": "ModelTimetable"},
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
    "credit_info": {"ja": "単位情報", "en": "Credit Information"},
    "required": {"ja": "必修", "en": "Required"},
    "elective": {"ja": "選択", "en": "Elective"},
    "credits": {"ja": "単位", "en": "credits"},
    "total": {"ja": "合計", "en": "Total"},
    "major1_courses": {"ja": "第1メジャー科目", "en": "1st Major Courses"},
    "shared_courses": {"ja": "情報学領域共有科目", "en": "Shared Information Science Courses"},
    "major2_courses": {"ja": "第2メジャー科目", "en": "2nd Major Courses"},
    "others_courses": {"ja": "その他メジャー科目", "en": "Other Major Courses"},
    "info_app_courses": {"ja": "情報応用科目", "en": "Information Application Courses"},
    "required_mandatory": {"ja": "必修/必履修", "en": "Required/Mandatory"},
    "elective_required_elective": {"ja": "選択・選択必修", "en": "Elective/Required Elective"},
    "credits_unit": {"ja": "単位数", "en": "Credits"},
    "total_simple": {"ja": "合計", "en": "Total"},
    "label_major1": {"ja": "Ⅰ", "en": "1st"},
    "label_shared": {"ja": "共", "en": "Shared"},
    "label_major2": {"ja": "Ⅱ", "en": "2nd"},
    "label_others": {"ja": "他", "en": "Other"},
    "label_info_app": {"ja": "応", "en": "Info"},
    "quarter_1": {"ja": "1Q", "en": "1Q"},
    "quarter_2": {"ja": "2Q", "en": "2Q"},
    "quarter_3": {"ja": "3Q", "en": "3Q"},
    "quarter_4": {"ja": "4Q", "en": "4Q"},
    "semester_first": {"ja": "前期", "en": "1st Sem"},
    "semester_second": {"ja": "後期", "en": "2nd Sem"},
    "credit_unit_badge": {"ja": "単位", "en": "cr"},
    "course_details": {"ja": "科目詳細", "en": "Course Details"},
    "course_name": {"ja": "科目名", "en": "Course Name"},
    "timetable_code": {"ja": "時間割コード", "en": "Timetable Code"},
    "instructor": {"ja": "担当教員", "en": "Instructor"},
    "credits_label": {"ja": "単位数", "en": "Credits"},
    "offering_period": {"ja": "開講区分", "en": "Offering Period"},
    "major_category": {"ja": "メジャー区分", "en": "Major Category"},
    "day_period": {"ja": "曜日・時限", "en": "Day & Period"},
    "classroom": {"ja": "教室", "en": "Classroom"},
    "syllabus_link": {"ja": "シラバスリンク", "en": "Syllabus Link"},
    "open_syllabus": {"ja": "シラバスを開く", "en": "Open Syllabus"},
    "close": {"ja": "閉じる", "en": "Close"},
    "select_priority": {"ja": "優先", "en": "Priority"},
    "multiple_courses_hint": {"ja": "複数の授業があります。優先する授業を選択してください。", "en": "Multiple courses available. Select priority course."},
    "intensive_courses": {"ja": "集中講義・実験実習", "en": "Intensive Courses & Labs"},
    "intensive_courses_note": {"ja": "※ 以下の科目は集中講義、実験・実習など、通常の時間割に含まれない科目です。", "en": "* The following courses are intensive courses, laboratory work, etc., which are not included in the regular timetable."},
    "class_format": {"ja": "授業形態", "en": "Class Format"},
    "course_type": {"ja": "授業種別", "en": "Course Type"},
}

CHOOSE = {
    "title": {"ja": "優先する科目の選択", "en": "Choosing Priority Subjects"},
    "schedule_conflicts": {"ja": "時間割の重複", "en": "Schedule Conflicts"},
    "conflicts_detected": {"ja": "以下の曜日・時限で複数の科目が重複しています。優先する科目を選択してください。", "en": "Multiple courses overlap at the following times. Please select the priority course."},
    "no_conflicts": {"ja": "時間割の重複はありません。", "en": "No schedule conflicts detected."},
    "select_priority_course": {"ja": "優先する科目を選択", "en": "Select Priority Course"},
    "apply_selections": {"ja": "選択を適用", "en": "Apply Selections"},
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
