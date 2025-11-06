# -*- coding: utf-8 -*-
"""
セメスタとメジャーに基づく科目検索
Query Courses by Semester and Major
"""

from typing import Optional, Set
from app import app
from src import db
from src.models import (
    Course,
    CourseSchedule,
    GradeYear,
    AffiliatedMajor,
    CourseClassroom,
)
from src.translations.field_values import (
    get_day_name,
    get_major_name,
    OfferingCategoryEnum,
)


def calculate_semester_from_grade_and_offering(min_grade: int, offering_category_id: int) -> Set[int]:
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


def query_courses_by_semester_and_major(semester: int, major_id: Optional[int] = None) -> None:
    """
    セメスタとメジャーを指定して、該当する科目の全情報を出力

    セメスタの計算ロジック:
    - 学年の最小値と開講区分から導出
    - セメスタ = (最小学年 - 1) × 2 + (前期なら1, 後期なら2)
    - 例: 2年前期 → (2-1)×2+1 = 3

    Args:
        semester: セメスタ（学期）1~8
        major_id: メジャーID（Noneの場合は全メジャー）
    """
    print("=" * 80)
    print("セメスタ・メジャー別科目検索")
    print("=" * 80)
    print(f"\n検索条件:")
    print(f"  セメスタ: {semester}")

    if major_id is not None:
        major_name = get_major_name(major_id)
        print(f"  メジャー: {major_name} (ID: {major_id})")
    else:
        print(f"  メジャー: 全メジャー")

    # セメスタから学年と学期を逆算
    target_grade = (semester - 1) // 2 + 1
    is_first_semester = (semester % 2 == 1)  # 奇数なら前期

    print(f"  → 対象学年: {target_grade}年以上")
    print(f"  → 対象学期: {'前期' if is_first_semester else '後期'}")

    # 科目を検索
    # 1. メジャーで絞り込み（指定がある場合）
    if major_id is not None:
        course_ids = db.session.query(AffiliatedMajor.timetable_code).filter(
            AffiliatedMajor.major_id == major_id
        ).distinct().all()
        course_ids = [c[0] for c in course_ids]

        if not course_ids:
            print("\n該当する科目が見つかりませんでした。")
            return

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
        course_semesters = calculate_semester_from_grade_and_offering(
            min_grade_value,
            course.offering_category_id
        )

        # 指定セメスタに該当するか確認
        if semester in course_semesters:
            matching_courses.append(course)

    if not matching_courses:
        print(f"\n該当する科目が見つかりませんでした。")
        return

    print(f"\n該当科目数: {len(matching_courses)}件")
    print("-" * 80)

    # 各科目の詳細情報を出力
    for idx, course in enumerate(matching_courses, 1):
        print(f"\n  [{idx}] {course.course_title}")
        print(f"      時間割コード: {course.timetable_code}")
        print(f"      単位数: {course.credits}")

        # シラバスURL
        if course.syllabus_url:
            print(f"      シラバスURL: {course.syllabus_url}")

        # 主担当教員
        if course.main_instructor:
            print(f"      主担当教員: {course.main_instructor.instructor_name}")

        # 開講曜限
        if course.schedules:
            schedules_str = []
            for schedule in course.schedules:
                day_name = get_day_name(schedule.day_id)
                schedules_str.append(f"{day_name}曜{schedule.period}限")
            print(f"      開講曜限: {', '.join(schedules_str)}")

        # 対象学年
        if course.grade_years:
            grades = sorted([grade.grade_name for grade in course.grade_years])
            print(f"      対象学年: {', '.join(grades)}年生")

        # 所属メジャーと履修区分
        if course.affiliated_majors:
            majors_info = []
            for affiliated in course.affiliated_majors:
                major_name = affiliated.major.major_name if affiliated.major else "不明"
                if affiliated.course_category:
                    category_name = affiliated.course_category.course_category_name
                    majors_info.append(f"{major_name}({category_name})")
                else:
                    majors_info.append(major_name)
            print(f"      所属メジャー: {', '.join(majors_info)}")

        # 使用教室
        if course.course_classrooms:
            classrooms = [cc.classroom.classroom_name for cc in course.course_classrooms]
            print(f"      使用教室: {', '.join(classrooms)}")

        # 授業形態
        if course.class_format:
            print(f"      授業形態: {course.class_format.class_format_name}")

        # 授業種別
        if course.course_type:
            print(f"      授業種別: {course.course_type.course_type_name}")

        # 開講区分
        if course.offering_category:
            print(f"      開講区分: {course.offering_category.offering_category_name}")

    print("\n" + "=" * 80)
    print(f"合計科目数: {len(matching_courses)}件")
    print("=" * 80)


def main():
    """メイン処理"""
    with app.app_context():
        print("\n")

        # 使用例1: セメスタのみ指定（全メジャー）
        print("【使用例1】セメスタ3（2年前期）の全科目を取得")
        query_courses_by_semester_and_major(semester=3)

        print("\n\n")

        # 使用例2: セメスタとメジャーを指定
        print("【使用例2】セメスタ3（2年前期）、ISメジャーの科目を取得")
        query_courses_by_semester_and_major(semester=3, major_id=1)

        print("\n\n")

        # 使用例3: セメスタ4（2年後期）
        print("【使用例3】セメスタ4（2年後期）、NCメジャーの科目を取得")
        query_courses_by_semester_and_major(semester=4, major_id=2)


if __name__ == '__main__':
    main()