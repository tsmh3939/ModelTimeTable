# -*- coding: utf-8 -*-
"""
シラバス用語の日英対訳辞書
Syllabus Terms Translation Dictionary (Japanese-English)
"""

# 基本情報
BASIC_INFO = {
    "開講科目名": "Course Title",
    "授業科目名": "Course Name",
    "時間割コード": "Timetable Code",
    "開講所属": "Offering Department",
    "ターム・学期": "Term/Semester",
    "学期": "Semester",
    "ターム": "Term",
    "曜限": "Day & Period",
    "曜日": "Day of Week",
    "時限": "Period",
    "開講区分": "Course Category",
    "単位数": "Credits",
    "学年": "Grade/Year",
    "主担当教員": "Main Instructor",
    "担当教員": "Instructor",
    "授業形態": "Class Format",
    "教室": "Classroom",
    "開講形態": "Course Type",
}

# ディプロマポリシー
DIPLOMA_POLICY = {
    "ディプロマポリシー情報": "Diploma Policy Information",
    "要件年度": "Requirement Year",
    "要件所属": "Requirement Affiliation",
    "ディプロマポリシー": "Diploma Policy",
    "DP値": "DP Value",
}

# 授業詳細
COURSE_DETAILS = {
    "授業の概要・ねらい": "Course Overview and Objectives",
    "授業概要": "Course Overview",
    "授業のねらい": "Course Objectives",
    "到達目標": "Learning Outcomes",
    "成績評価の方法・基準": "Grading Method and Criteria",
    "成績評価": "Grading",
    "評価方法": "Evaluation Method",
    "評価基準": "Evaluation Criteria",
    "教科書": "Textbook",
    "参考書・参考文献": "Reference Books and Materials",
    "参考書": "Reference Books",
    "参考文献": "References",
    "履修上の注意・メッセージ": "Notes and Messages for Students",
    "履修上の注意": "Course Notes",
    "メッセージ": "Message",
    "履修する上で必要な事項": "Prerequisites",
    "必要な事項": "Requirements",
    "履修を推奨する関連科目": "Recommended Related Courses",
    "関連科目": "Related Courses",
    "授業時間外学修についての指示": "Instructions for Out-of-Class Learning",
    "授業時間外学修": "Out-of-Class Learning",
    "その他連絡事項": "Other Information",
    "連絡事項": "Contact Information",
    "授業理解を深める方法": "Methods to Deepen Understanding",
    "オフィスアワー": "Office Hours",
    "科目ナンバリング": "Course Numbering",
    "実務経験": "Professional Experience",
}

# 授業計画
SCHEDULE = {
    "授業計画": "Course Schedule",
    "No.": "No.",
    "回": "Session",
    "日時": "Date/Time",
    "主題と位置付け": "Topic and Context",
    "主題": "Topic",
    "位置付け": "Context",
    "学習方法と内容": "Learning Method and Content",
    "学習方法": "Learning Method",
    "学習内容": "Learning Content",
    "備考": "Notes",
    "担当": "Instructor",
}

# 一般用語
COMMON_TERMS = {
    # 学期
    "前期": "First Semester",
    "後期": "Second Semester",
    "通年": "Full Year",
    "集中": "Intensive",
    # 科目区分
    "必修": "Required",
    "選択": "Elective",
    "選択必修": "Required Elective",
    # 授業形態
    "講義": "Lecture",
    "演習": "Seminar",
    "実験": "Experiment",
    "実習": "Practical Training",
    "卒業研究": "Graduation Research",
    # 開講形態
    "対面": "Face-to-Face",
    "遠隔": "Remote",
    "ハイブリッド": "Hybrid",
    "オンデマンド": "On-Demand",
    "同時双方向": "Synchronous Interactive",
    # 曜日
    "月曜日": "Monday",
    "火曜日": "Tuesday",
    "水曜日": "Wednesday",
    "木曜日": "Thursday",
    "金曜日": "Friday",
    "土曜日": "Saturday",
    "日曜日": "Sunday",
    "月": "Mon",
    "火": "Tue",
    "水": "Wed",
    "木": "Thu",
    "金": "Fri",
    "土": "Sat",
    "日": "Sun",
    # 時限
    "1限": "1st Period",
    "2限": "2nd Period",
    "3限": "3rd Period",
    "4限": "4th Period",
    "5限": "5th Period",
    "6限": "6th Period",
    "7限": "7th Period",
}

# アクション
ACTIONS = {
    "戻る": "Back",
    "印刷": "Print",
    "検索": "Search",
    "登録": "Register",
    "編集": "Edit",
    "削除": "Delete",
    "保存": "Save",
    "キャンセル": "Cancel",
    "確認": "Confirm",
    "送信": "Submit",
    "ダウンロード": "Download",
    "アップロード": "Upload",
}

# すべての用語を統合
ALL_TERMS = {
    **BASIC_INFO,
    **DIPLOMA_POLICY,
    **COURSE_DETAILS,
    **SCHEDULE,
    **COMMON_TERMS,
    **ACTIONS,
}


def translate(japanese_term: str) -> str:
    """
    日本語用語を英語に翻訳

    Args:
        japanese_term: 日本語用語

    Returns:
        英語訳（見つからない場合は元の用語）
    """
    return ALL_TERMS.get(japanese_term, japanese_term)


def get_category_terms(category: str) -> dict:
    """
    カテゴリ別の用語辞書を取得

    Args:
        category: カテゴリ名 ('basic_info', 'course_details', 'schedule', 'common_terms', 'actions')

    Returns:
        カテゴリ別の用語辞書
    """
    categories = {
        'basic_info': BASIC_INFO,
        'diploma_policy': DIPLOMA_POLICY,
        'course_details': COURSE_DETAILS,
        'schedule': SCHEDULE,
        'common_terms': COMMON_TERMS,
        'actions': ACTIONS,
    }
    return categories.get(category, {})
