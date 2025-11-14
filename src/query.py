# -*- coding: utf-8 -*-
"""
セメスタとメジャーに基づく科目検索
Query Courses by Semester and Major
"""

from typing import Optional, Set
from src import db
from src.models import Course, AffiliatedMajor
from src.translations.field_values import OfferingCategoryEnum


def calculate_semester(min_grade: int, offering_category_id: int) -> Set[int]:
    """
    学年の最小値と開講区分からセメスタを計算

    Args:
        min_grade: 学年の最小値（例: 2, 3, 4）
        offering_category_id: 開講区分ID

    Returns:
        該当するセメスタのセット（複数の場合あり）
    """
    semesters = set()

    # 基準値: (学年 - 1) × 2
    base = (min_grade - 1) * 2

    if offering_category_id == OfferingCategoryEnum.FULL_YEAR:
        # 通年: 前期・後期両方
        semesters.add(base + 1)
        semesters.add(base + 2)
    elif offering_category_id in [
        OfferingCategoryEnum.FIRST_QUARTER,
        OfferingCategoryEnum.SECOND_QUARTER,
        OfferingCategoryEnum.FIRST_SEMESTER,
    ]:
        # 1Q, 2Q, 前期 → 奇数セメスタ
        semesters.add(base + 1)
    elif offering_category_id in [
        OfferingCategoryEnum.THIRD_QUARTER,
        OfferingCategoryEnum.FOURTH_QUARTER,
        OfferingCategoryEnum.SECOND_SEMESTER,
    ]:
        # 3Q, 4Q, 後期 → 偶数セメスタ
        semesters.add(base + 2)

    return semesters

def get_courses_by_semester_and_major(semester: int, major_id: Optional[int] = None) -> list:
    """
    セメスタとメジャーを指定して、該当する科目のリストを返す

    Args:
        semester: セメスタ（学期）1~8
        major_id: メジャーID（Noneの場合は全メジャー）

    Returns:
        該当する科目のリスト
    """
    # 科目を検索
    # 1. メジャーで絞り込み（指定がある場合）
    if major_id is not None:
        course_ids = db.session.query(AffiliatedMajor.timetable_code).filter(
            AffiliatedMajor.major_id == major_id
        ).distinct().all()
        course_ids = [c[0] for c in course_ids]

        if not course_ids:
            return []

        query = Course.query.filter(Course.timetable_code.in_(course_ids))
    else:
        query = Course.query

    all_courses = query.all()

    # 2. 各科目について、学年と開講区分からセメスタを計算してフィルタリング
    matching_courses = []

    for course in all_courses:
        # 学年の最小値を取得
        if not course.grade_years:
            continue

        min_grade_value = min(int(gy.grade_name) for gy in course.grade_years)

        # 開講区分IDを取得
        if course.offering_category_id is None:
            continue

        # セメスタを計算
        course_semesters = calculate_semester(
            min_grade_value,
            course.offering_category_id
        )

        # 指定セメスタに該当するか確認
        if semester in course_semesters:
            matching_courses.append(course)

    return matching_courses
