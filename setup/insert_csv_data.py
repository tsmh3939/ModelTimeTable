#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
変換済みCSVデータをデータベースにインポートするスクリプト
Import Converted CSV Data to Database
"""

import sys
import csv
from app import app
from src import db
from src.models import (
    Course,
    CourseSchedule,
    GradeYear,
    AffiliatedMajor,
    CourseClassroom,
    InstructorMaster,
    ClassroomMaster,
)


def import_instructor_master(csv_path: str) -> None:
    """教員マスタをインポート"""
    print("\n教員マスタをインポート中...")
    count = 0

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            instructor_id = int(row['教員ID'])
            instructor_name = row['教員名'].strip()

            existing = InstructorMaster.query.filter_by(instructor_id=instructor_id).first()
            if not existing:
                instructor = InstructorMaster(
                    instructor_id=instructor_id,  # pyright: ignore[reportCallIssue]
                    instructor_name=instructor_name  # pyright: ignore[reportCallIssue]
                )
                db.session.add(instructor)
                count += 1
                print(f"  追加: {instructor_id} - {instructor_name}")
            else:
                print(f"  スキップ: {instructor_id} - {instructor_name} (既存)")

    print(f"教員マスタ: {count}件追加")


def import_classroom_master(csv_path: str) -> None:
    """教室マスタをインポート"""
    print("\n教室マスタをインポート中...")
    count = 0

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            classroom_id = int(row['教室ID'])
            classroom_name = row['教室名'].strip()

            existing = ClassroomMaster.query.filter_by(classroom_id=classroom_id).first()
            if not existing:
                classroom = ClassroomMaster(
                    classroom_id=classroom_id,  # pyright: ignore[reportCallIssue]
                    classroom_name=classroom_name  # pyright: ignore[reportCallIssue]
                )
                db.session.add(classroom)
                count += 1
                print(f"  追加: {classroom_id} - {classroom_name}")
            else:
                print(f"  スキップ: {classroom_id} - {classroom_name} (既存)")

    print(f"教室マスタ: {count}件追加")


def import_courses(csv_path: str) -> None:
    """科目をインポート"""
    print("\n科目をインポート中...")
    count = 0

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['timetable_code'].strip()

            existing = Course.query.filter_by(timetable_code=timetable_code).first()
            if not existing:
                course = Course(
                    timetable_code=timetable_code,  # pyright: ignore[reportCallIssue]
                    syllabus_url=row['syllabus_url'].strip() or None,  # pyright: ignore[reportCallIssue]
                    course_title=row['course_title'].strip(),  # pyright: ignore[reportCallIssue]
                    credits=int(row['credits']),  # pyright: ignore[reportCallIssue]
                    offering_category_id=int(row['offering_category_id']) if row['offering_category_id'] else None,  # pyright: ignore[reportCallIssue]
                    class_format_id=int(row['class_format_id']) if row['class_format_id'] else None,  # pyright: ignore[reportCallIssue]
                    course_type_id=int(row['course_type_id']) if row['course_type_id'] else None,  # pyright: ignore[reportCallIssue]
                    main_instructor_id=int(row['main_instructor_id']) if row['main_instructor_id'] else None,  # pyright: ignore[reportCallIssue]
                )
                db.session.add(course)
                count += 1
                print(f"  追加: {timetable_code} - {row['course_title']}")
            else:
                print(f"  スキップ: {timetable_code} (既存)")

    print(f"科目: {count}件追加")


def import_course_schedules(csv_path: str) -> None:
    """開講曜限をインポート"""
    print("\n開講曜限をインポート中...")
    count = 0

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['timetable_code'].strip()
            day_id = int(row['day_id'])
            period = int(row['period'])

            existing = CourseSchedule.query.filter_by(
                timetable_code=timetable_code,
                day_id=day_id,
                period=period
            ).first()

            if not existing:
                schedule = CourseSchedule(
                    timetable_code=timetable_code,  # pyright: ignore[reportCallIssue]
                    day_id=day_id,  # pyright: ignore[reportCallIssue]
                    period=period  # pyright: ignore[reportCallIssue]
                )
                db.session.add(schedule)
                count += 1
            else:
                print(f"  スキップ: {timetable_code} 曜日ID:{day_id} (既存)")

    print(f"開講曜限: {count}件追加")


def import_grade_years(csv_path: str) -> None:
    """学年をインポート"""
    print("\n学年をインポート中...")
    count = 0

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['時間割コード'].strip()
            grade_name = row['学年名'].strip()

            existing = GradeYear.query.filter_by(
                timetable_code=timetable_code,
                grade_name=grade_name
            ).first()

            if not existing:
                grade = GradeYear(
                    timetable_code=timetable_code,  # pyright: ignore[reportCallIssue]
                    grade_name=grade_name  # pyright: ignore[reportCallIssue]
                )
                db.session.add(grade)
                count += 1
            else:
                print(f"  スキップ: {timetable_code} 学年:{grade_name} (既存)")

    print(f"学年: {count}件追加")


def import_affiliated_majors(csv_path: str) -> None:
    """所属メジャーをインポート"""
    print("\n所属メジャーをインポート中...")
    count = 0

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['timetable_code'].strip()
            major_id = int(row['major_id'])
            course_category_id = int(row['course_category_id']) if row['course_category_id'] else None

            existing = AffiliatedMajor.query.filter_by(
                timetable_code=timetable_code,
                major_id=major_id
            ).first()

            if not existing:
                affiliated = AffiliatedMajor(
                    timetable_code=timetable_code,  # pyright: ignore[reportCallIssue]
                    major_id=major_id,  # pyright: ignore[reportCallIssue]
                    course_category_id=course_category_id  # pyright: ignore[reportCallIssue]
                )
                db.session.add(affiliated)
                count += 1
            else:
                print(f"  スキップ: {timetable_code} メジャーID:{major_id} (既存)")

    print(f"所属メジャー: {count}件追加")


def import_course_classrooms(csv_path: str) -> None:
    """科目教室をインポート"""
    print("\n科目教室をインポート中...")
    count = 0

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['timetable_code'].strip()
            classroom_id = int(row['classroom_id'])

            existing = CourseClassroom.query.filter_by(
                timetable_code=timetable_code,
                classroom_id=classroom_id
            ).first()

            if not existing:
                course_classroom = CourseClassroom(
                    timetable_code=timetable_code,  # pyright: ignore[reportCallIssue]
                    classroom_id=classroom_id  # pyright: ignore[reportCallIssue]
                )
                db.session.add(course_classroom)
                count += 1
            else:
                print(f"  スキップ: {timetable_code} 教室ID:{classroom_id} (既存)")

    print(f"科目教室: {count}件追加")


def insert():
    """メイン処理"""
    with app.app_context():
        print("=" * 60)
        print("CSVデータインポート開始")
        print("=" * 60)

        converted_dir = 'docs/converted'

        try:
            # マスタデータを先にインポート
            import_instructor_master(f'{converted_dir}/instructor_master.csv')
            import_classroom_master(f'{converted_dir}/classroom_master.csv')

            # 科目データをインポート（外部キー依存）
            import_courses(f'{converted_dir}/course.csv')

            # 中間テーブルをインポート（科目データ依存）
            import_course_schedules(f'{converted_dir}/course_schedule.csv')
            import_grade_years(f'{converted_dir}/grade_year.csv')
            import_affiliated_majors(f'{converted_dir}/affiliated_major.csv')
            import_course_classrooms(f'{converted_dir}/course_classroom.csv')

            # コミット
            db.session.commit()

            print("\n" + "=" * 60)
            print("✓ CSVデータインポート完了")
            print("=" * 60)

            # データ確認
            print("\n【データ確認】")
            print(f"教員マスタ: {InstructorMaster.query.count()}件")
            print(f"教室マスタ: {ClassroomMaster.query.count()}件")
            print(f"科目: {Course.query.count()}件")
            print(f"開講曜限: {CourseSchedule.query.count()}件")
            print(f"学年: {GradeYear.query.count()}件")
            print(f"所属メジャー: {AffiliatedMajor.query.count()}件")
            print(f"科目教室: {CourseClassroom.query.count()}件")

        except Exception as e:
            db.session.rollback()
            print(f"\n✗ エラーが発生しました: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    insert()