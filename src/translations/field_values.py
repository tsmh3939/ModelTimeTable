# -*- coding: utf-8 -*-
"""
フィールド値の定義と翻訳
Field Values Definitions and Translations
"""

from enum import IntEnum
from typing import Dict, List


# 時限の値
# 0は曜日が「他」の場合
PERIODS = [0, 1, 2, 3, 4, 5, 6]

# セメスタの値
SEMESTERS = {
    3: {"ja": "2年前期", "en": "2nd Year 1st Semester"},
    4: {"ja": "2年後期", "en": "2nd Year 2nd Semester"},
    5: {"ja": "3年前期", "en": "3rd Year 1st Semester"},
    6: {"ja": "3年後期", "en": "3rd Year 2nd Semester"}
}

# 単位数の値
# 1,2以外は卒業研究のみ
CREDITS = [1, 2, 8]

# 学年の値（Grade/Year values）
GRADES = [1, 2, 3, 4]


class CourseCategoryEnum(IntEnum):
    """履修区分マスタ / Course Category Master"""
    REQUIRED = 1           # 必修
    REQUIRED_ELECTIVE = 2  # 選択必修
    ELECTIVE = 3           # 選択
    MANDATORY = 4          # 必履修


class OfferingCategoryEnum(IntEnum):
    """開講区分マスタ / Offering Category Master"""
    FULL_YEAR = 0          # 通年
    FIRST_QUARTER = 1      # 1Q
    SECOND_QUARTER = 2     # 2Q
    THIRD_QUARTER = 3      # 3Q
    FOURTH_QUARTER = 4     # 4Q
    FIRST_SEMESTER = 5     # 前期
    SECOND_SEMESTER = 6    # 後期


class DayEnum(IntEnum):
    """曜日マスタ / Day Master"""
    OTHER = 0     # 他
    MONDAY = 1    # 月
    TUESDAY = 2   # 火
    WEDNESDAY = 3 # 水
    THURSDAY = 4  # 木
    FRIDAY = 5    # 金
    SATURDAY = 6  # 土


class MajorEnum(IntEnum):
    """メジャーマスタ / Major Master"""
    IS = 1  # IS
    NC = 2  # NC
    XD = 3  # XD


class ClassFormatEnum(IntEnum):
    """授業形態マスタ / Class Format Master"""
    LECTURE = 1           # 講義
    SEMINAR = 2           # 演習
    EXPERIMENT = 3        # 実験
    LECTURE_SEMINAR = 4   # 講義・演習


class CourseTypeEnum(IntEnum):
    """授業種別マスタ / Course Type Master"""
    REGULAR = 1           # 普通
    INTENSIVE = 2         # 集中
    EXPERIMENT_PRACTICE = 3  # 実験・実習


# 履修区分マスタ（Course Category Master）
COURSE_CATEGORY_MASTER = {
    1: {"ja": "必修", "en": "Required"},
    2: {"ja": "選択必修", "en": "Required Elective"},
    3: {"ja": "選択", "en": "Elective"},
    4: {"ja": "必履修", "en": "Mandatory"},
}

# 開講区分マスタ（Offering Category Master）
OFFERING_CATEGORY_MASTER = {
    0: {"ja": "通年", "en": "Full Year"},
    1: {"ja": "1Q", "en": "1st Quarter"},
    2: {"ja": "2Q", "en": "2nd Quarter"},
    3: {"ja": "3Q", "en": "3rd Quarter"},
    4: {"ja": "4Q", "en": "4th Quarter"},
    5: {"ja": "前期", "en": "First Semester"},
    6: {"ja": "後期", "en": "Second Semester"},
}

# 曜日マスタ（Day Master）
DAY_MASTER = {
    0: {"ja": "他", "en": "Other"},
    1: {"ja": "月", "en": "Monday"},
    2: {"ja": "火", "en": "Tuesday"},
    3: {"ja": "水", "en": "Wednesday"},
    4: {"ja": "木", "en": "Thursday"},
    5: {"ja": "金", "en": "Friday"},
    6: {"ja": "土", "en": "Saturday"},
}

# 曜日マスタ（短縮形）
DAY_MASTER_SHORT = {
    0: {"ja": "他", "en": "Other"},
    1: {"ja": "月", "en": "Mon"},
    2: {"ja": "火", "en": "Tue"},
    3: {"ja": "水", "en": "Wed"},
    4: {"ja": "木", "en": "Thu"},
    5: {"ja": "金", "en": "Fri"},
    6: {"ja": "土", "en": "Sat"},
}

# メジャーマスタ（Major Master）
MAJOR_MASTER = {
    1: {"ja": "IS", "en": "IS"},
    2: {"ja": "NC", "en": "NC"},
    3: {"ja": "XD", "en": "XD"},
}

# 授業形態マスタ（Class Format Master）
CLASS_FORMAT_MASTER = {
    1: {"ja": "講義", "en": "Lecture"},
    2: {"ja": "演習", "en": "Seminar"},
    3: {"ja": "実験", "en": "Experiment"},
    4: {"ja": "講義・演習", "en": "Lecture & Seminar"},
}

# 授業種別マスタ（Course Type Master）
COURSE_TYPE_MASTER = {
    1: {"ja": "普通", "en": "Regular"},
    2: {"ja": "集中", "en": "Intensive"},
    3: {"ja": "実験・実習", "en": "Experiment & Practice"},
}

# 特殊値
CLASSROOM_UNDECIDED = {"ja": "未定", "en": "TBD"}


def get_course_category_name(category_id: int, lang: str = 'ja') -> str:
    """
    履修区分IDから名称を取得

    Args:
        category_id: 履修区分ID (1-4)
        lang: 言語 ('ja' or 'en')

    Returns:
        履修区分名
    """
    return COURSE_CATEGORY_MASTER.get(category_id, {}).get(lang, str(category_id))


def get_offering_category_name(category_id: int, lang: str = 'ja') -> str:
    """
    開講区分IDから名称を取得

    Args:
        category_id: 開講区分ID (0-6)
        lang: 言語 ('ja' or 'en')

    Returns:
        開講区分名
    """
    return OFFERING_CATEGORY_MASTER.get(category_id, {}).get(lang, str(category_id))


def get_day_name(day_id: int, lang: str = 'ja', short: bool = False) -> str:
    """
    曜日IDから名称を取得

    Args:
        day_id: 曜日ID (0-6)
        lang: 言語 ('ja' or 'en')
        short: 短縮形を使用するか

    Returns:
        曜日名
    """
    master = DAY_MASTER_SHORT if short else DAY_MASTER
    return master.get(day_id, {}).get(lang, str(day_id))


def get_major_name(major_id: int, lang: str = 'ja') -> str:
    """
    メジャーIDから名称を取得

    Args:
        major_id: メジャーID (1-3)
        lang: 言語 ('ja' or 'en')

    Returns:
        メジャー名
    """
    return MAJOR_MASTER.get(major_id, {}).get(lang, str(major_id))


def get_class_format_name(format_id: int, lang: str = 'ja') -> str:
    """
    授業形態IDから名称を取得

    Args:
        format_id: 授業形態ID (1-4)
        lang: 言語 ('ja' or 'en')

    Returns:
        授業形態名
    """
    return CLASS_FORMAT_MASTER.get(format_id, {}).get(lang, str(format_id))


def get_course_type_name(type_id: int, lang: str = 'ja') -> str:
    """
    授業種別IDから名称を取得

    Args:
        type_id: 授業種別ID (1-3)
        lang: 言語 ('ja' or 'en')

    Returns:
        授業種別名
    """
    return COURSE_TYPE_MASTER.get(type_id, {}).get(lang, str(type_id))


def get_classroom_undecided(lang: str = 'ja') -> str:
    """
    教室未定の表示を取得

    Args:
        lang: 言語 ('ja' or 'en')

    Returns:
        未定の表示
    """
    return CLASSROOM_UNDECIDED.get(lang, "TBD")


def get_semester_name(semester_id: int, lang: str = 'ja') -> str:
    """
    セメスタIDから名称を取得

    Args:
        semester_id: セメスタID (3-6)
        lang: 言語 ('ja' or 'en')

    Returns:
        セメスタ名
    """
    return SEMESTERS.get(semester_id, {}).get(lang, str(semester_id))