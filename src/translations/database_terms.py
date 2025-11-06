# -*- coding: utf-8 -*-
"""
データベーステーブル・フィールドの日英対訳辞書
Database Terms Translation Dictionary (Japanese-English)
"""

# テーブル名（日本語 → 英語クラス名）
TABLES = {
    "時間割科目": "TimetableSubject",
    "時間割モデル": "TimetableModel",
    "開講曜限": "CourseSchedule",
    "曜日マスタ": "DayMaster",
    "学年": "GradeYear",
    "メジャーマスタ": "MajorMaster",
    "科目": "Course",
    "科目教室": "CourseClassroom",
    "教室マスタ": "ClassroomMaster",
    "科目教員": "CourseInstructor",
    "教員マスタ": "InstructorMaster",
    "所属メジャー": "AffiliatedMajor",
    "履修区分マスタ": "CourseCategoryMaster",
    "開講区分マスタ": "OfferingCategoryMaster",
    "授業形態マスタ": "ClassFormatMaster",
    "授業種別マスタ": "CourseTypeMaster",
}

# フィールド名（日本語 → snake_case）
FIELDS = {
    "時間割モデルID": "timetable_model_id",
    "時間割コード": "timetable_code",
    "セメスタ": "semester",
    "第1メジャーID": "major1_id",
    "第2メジャーID": "major2_id",
    "曜日ID": "day_id",
    "曜日名": "day_name",
    "時限": "period",
    "学年名": "grade_name",
    "メジャーID": "major_id",
    "メジャー名": "major_name",
    "開講科目名": "course_title",
    "単位数": "credits",
    "履修区分ID": "course_category_id",
    "履修区分名": "course_category_name",
    "開講区分ID": "offering_category_id",
    "開講区分名": "offering_category_name",
    "授業形態ID": "class_format_id",
    "授業形態名": "class_format_name",
    "授業種別ID": "course_type_id",
    "授業種別名": "course_type_name",
    "主担当教員ID": "main_instructor_id",
    "教室ID": "classroom_id",
    "教室名": "classroom_name",
    "教員ID": "instructor_id",
    "教員名": "instructor_name",
}

# フィールドラベル（日本語 → 英語表示名）
FIELD_LABELS = {
    "時間割モデルID": "Timetable Model ID",
    "時間割コード": "Timetable Code",
    "セメスタ": "Semester",
    "第1メジャーID": "First Major ID",
    "第2メジャーID": "Second Major ID",
    "曜日ID": "Day ID",
    "曜日名": "Day Name",
    "時限": "Period",
    "学年名": "Grade/Year Name",
    "メジャーID": "Major ID",
    "メジャー名": "Major Name",
    "開講科目名": "Course Title",
    "単位数": "Credits",
    "履修区分ID": "Course Category ID",
    "履修区分名": "Course Category Name",
    "開講区分ID": "Offering Category ID",
    "開講区分名": "Offering Category Name",
    "授業形態ID": "Class Format ID",
    "授業形態名": "Class Format Name",
    "授業種別ID": "Course Type ID",
    "授業種別名": "Course Type Name",
    "主担当教員ID": "Main Instructor ID",
    "教室ID": "Classroom ID",
    "教室名": "Classroom Name",
    "教員ID": "Instructor ID",
    "教員名": "Instructor Name",
}

# テーブル説明（英語）
TABLE_DESCRIPTIONS = {
    "TimetableSubject": "Junction table linking timetable models to courses",
    "TimetableModel": "Timetable configuration model for each semester",
    "CourseSchedule": "Course schedule information with day of week and period",
    "DayMaster": "Master table for days of the week",
    "GradeYear": "Target grade/year levels for courses",
    "MajorMaster": "Master table for academic majors/programs",
    "Course": "Main course information table",
    "CourseClassroom": "Junction table linking courses to classrooms",
    "ClassroomMaster": "Master table for classroom information",
    "CourseInstructor": "Junction table linking courses to instructors",
    "InstructorMaster": "Master table for instructor information",
    "AffiliatedMajor": "Junction table linking courses to majors",
    "CourseCategoryMaster": "Master table for course categories (required/elective)",
    "OfferingCategoryMaster": "Master table for offering categories",
    "ClassFormatMaster": "Master table for class formats (lecture/seminar/etc)",
    "CourseTypeMaster": "Master table for course types",
}


def translate_table(japanese_name: str) -> str:
    """
    テーブル名を日本語から英語に翻訳

    Args:
        japanese_name: 日本語テーブル名

    Returns:
        英語テーブル名（見つからない場合は元の名前）
    """
    return TABLES.get(japanese_name, japanese_name)


def translate_field(japanese_name: str) -> str:
    """
    フィールド名を日本語からsnake_caseに翻訳

    Args:
        japanese_name: 日本語フィールド名

    Returns:
        snake_case形式のフィールド名（見つからない場合は元の名前）
    """
    return FIELDS.get(japanese_name, japanese_name)


def translate_field_label(japanese_name: str) -> str:
    """
    フィールド名を日本語から英語ラベルに翻訳

    Args:
        japanese_name: 日本語フィールド名

    Returns:
        英語ラベル（見つからない場合は元の名前）
    """
    return FIELD_LABELS.get(japanese_name, japanese_name)


def get_table_description(english_table_name: str) -> str:
    """
    テーブルの説明を取得

    Args:
        english_table_name: 英語テーブル名

    Returns:
        テーブルの説明（見つからない場合は空文字列）
    """
    return TABLE_DESCRIPTIONS.get(english_table_name, "")