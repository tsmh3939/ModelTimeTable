# -*- coding: utf-8 -*-
"""
Additional.txtに記載された課題の解答例

課題1：第1メジャー：IS で3年後期に割り当てられている第1メジャー科目を全て出力
課題2：第1メジャー：IS、第2メジャー：NC で3年後期に割り当てられている第2メジャー科目を全て出力（IS科目除外）
"""

import os
from datetime import datetime
from app import app
from src import db
from src.models import (
    Course,
    CourseSchedule,
    DayMaster,
    InstructorMaster,
    CourseInstructor,
    CourseCategoryMaster,
    AffiliatedMajor,
    GradeYear,
    MajorMaster,
    OfferingCategoryMaster,
)
from sqlalchemy import text
from sqlalchemy.orm import aliased


# 出力ディレクトリの設定
OUTPUT_DIR = 'docs/query_results'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def query1_sql(major_name='IS', grade='3', semester='後期'):
    """
    課題1：SQLによる直接クエリ

    第1メジャー科目（科目名，曜日時限，主担当教員，必修・選択必修・選択の別）を全て出力

    Args:
        major_name: メジャー名（デフォルト: 'IS'）
        grade: 学年名（デフォルト: '3'）
        semester: 学期（デフォルト: '後期'、選択肢: '前期', '後期', '通年'）
    """
    print("=" * 80)
    print(f"課題1：SQL直接クエリ - {major_name}メジャー {grade}年{semester}")
    print("=" * 80)

    # 学期に応じた開講区分を決定
    if semester == '前期':
        offering_categories = ['1Q', '2Q', '前期']
    elif semester == '後期':
        offering_categories = ['3Q', '4Q', '後期']
    else:  # 通年
        offering_categories = ['通年']

    # SQLiteのIN句用にプレースホルダーを動的に生成
    placeholders = ', '.join([f':cat{i}' for i in range(len(offering_categories))])

    sql = text(f"""
        SELECT DISTINCT
            c.course_title AS 科目名,
            d.day_name AS 曜日名,
            cs.period AS 時限,
            main_inst.instructor_name AS 主担当教員,
            cc.course_category_name AS 履修区分
        FROM course c
        INNER JOIN course_schedule cs ON c.timetable_code = cs.timetable_code
        INNER JOIN day_master d ON cs.day_id = d.day_id
        INNER JOIN instructor_master main_inst ON c.main_instructor_id = main_inst.instructor_id
        INNER JOIN affiliated_major am ON c.timetable_code = am.timetable_code
        INNER JOIN major_master mm ON am.major_id = mm.major_id
        LEFT JOIN course_category_master cc ON am.course_category_id = cc.course_category_id
        INNER JOIN offering_category_master oc ON c.offering_category_id = oc.offering_category_id
        WHERE mm.major_name = :major_name
        AND oc.offering_category_name IN ({placeholders})
        AND c.timetable_code IN (
            SELECT gy2.timetable_code
            FROM grade_year gy2
            WHERE gy2.timetable_code = c.timetable_code
            GROUP BY gy2.timetable_code
            HAVING MIN(gy2.grade_name) = :grade
        )
        ORDER BY d.day_id, cs.period, c.course_title
    """)

    # パラメータを構築
    params = {
        'major_name': major_name,
        'grade': grade,
    }
    for i, cat in enumerate(offering_categories):
        params[f'cat{i}'] = cat

    with app.app_context():
        result = db.session.execute(sql, params)

        # ファイル名の生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{OUTPUT_DIR}/query1_sql_{major_name}_{grade}_{semester}_{timestamp}.md"

        # 結果をリストに変換
        rows = list(result)

        # コンソールとファイルの両方に出力
        output_lines = []
        output_lines.append(f"\n## 検索条件")
        output_lines.append(f"- メジャー: {major_name}")
        output_lines.append(f"- 学年: {grade}")
        output_lines.append(f"- 学期: {semester}")
        output_lines.append("")

        # マークダウンテーブルのヘッダー
        output_lines.append("| 科目名 | 曜日 | 時限 | 主担当教員 | 履修区分 |")
        output_lines.append("|--------|------|------|------------|----------|")

        # データ行
        for row in rows:
            course_category = row.履修区分 or '(未設定)'
            line = f"| {row.科目名} | {row.曜日名} | {row.時限} | {row.主担当教員} | {course_category} |"
            output_lines.append(line)

        output_lines.append("")
        output_lines.append(f"**合計: {len(rows)}件**")
        output_lines.append("")

        # コンソールに出力
        for line in output_lines:
            print(line)

        # ファイルに保存
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))

        print(f"結果を保存しました: {filename}\n")


def query1_sqlalchemy(major_name='IS', grade='3', semester='後期'):
    """
    課題1：SQLAlchemyによるクエリ

    第1メジャー科目（科目名，曜日時限，主担当教員，主でない教員，必修・選択必修・選択の別）を全て出力

    Args:
        major_name: メジャー名（デフォルト: 'IS'）
        grade: 学年名（デフォルト: '3'）
        semester: 学期（デフォルト: '後期'、選択肢: '前期', '後期', '通年'）
    """
    print("=" * 80)
    print(f"課題1：SQLAlchemy - {major_name}メジャー {grade}年{semester}")
    print("=" * 80)

    # 学期に応じた開講区分を決定
    if semester == '前期':
        offering_categories = ['1Q', '2Q', '前期']
    elif semester == '後期':
        offering_categories = ['3Q', '4Q', '後期']
    else:  # 通年
        offering_categories = ['通年']

    with app.app_context():
        from sqlalchemy import func

        # 学年の最小値を持つ科目のサブクエリ
        min_grade_subquery = db.session.query(
            GradeYear.timetable_code
        ).group_by(
            GradeYear.timetable_code
        ).having(
            func.min(GradeYear.grade_name) == grade
        ).subquery()

        # メインクエリ
        query = db.session.query(
            Course.course_title,
            DayMaster.day_name,
            CourseSchedule.period,
            InstructorMaster.instructor_name.label('main_instructor'),
            CourseCategoryMaster.course_category_name
        ).join(
            CourseSchedule, Course.timetable_code == CourseSchedule.timetable_code
        ).join(
            DayMaster, CourseSchedule.day_id == DayMaster.day_id
        ).join(
            InstructorMaster, Course.main_instructor_id == InstructorMaster.instructor_id
        ).join(
            AffiliatedMajor, Course.timetable_code == AffiliatedMajor.timetable_code
        ).join(
            MajorMaster, AffiliatedMajor.major_id == MajorMaster.major_id
        ).outerjoin(
            CourseCategoryMaster, AffiliatedMajor.course_category_id == CourseCategoryMaster.course_category_id
        ).join(
            OfferingCategoryMaster, Course.offering_category_id == OfferingCategoryMaster.offering_category_id
        ).filter(
            MajorMaster.major_name == major_name,
            Course.timetable_code.in_(min_grade_subquery),
            OfferingCategoryMaster.offering_category_name.in_(offering_categories)
        ).order_by(
            DayMaster.day_id,
            CourseSchedule.period,
            Course.course_title
        ).distinct()

        results = query.all()

        # ファイル名の生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{OUTPUT_DIR}/query1_sqlalchemy_{major_name}_{grade}_{semester}_{timestamp}.md"

        # コンソールとファイルの両方に出力
        output_lines = []
        output_lines.append(f"\n## 検索条件")
        output_lines.append(f"- メジャー: {major_name}")
        output_lines.append(f"- 学年: {grade}")
        output_lines.append(f"- 学期: {semester}")
        output_lines.append("")

        # マークダウンテーブルのヘッダー
        output_lines.append("| 科目名 | 曜日 | 時限 | 主担当教員 | 履修区分 |")
        output_lines.append("|--------|------|------|------------|----------|")

        # データ行
        for row in results:
            course_category = row.course_category_name or '(未設定)'
            line = f"| {row.course_title} | {row.day_name} | {row.period} | {row.main_instructor} | {course_category} |"
            output_lines.append(line)

        output_lines.append("")
        output_lines.append(f"**合計: {len(results)}件**")
        output_lines.append("")

        # コンソールに出力
        for line in output_lines:
            print(line)

        # ファイルに保存
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))

        print(f"結果を保存しました: {filename}\n")


def query2_sql(major1_name='IS', major2_name='NC', grade='3', semester='後期'):
    """
    課題2：SQLによる直接クエリ

    第2メジャー科目（科目名，曜日時限，主担当教員，必修・選択必修・選択の別）を全て出力
    第1メジャー・第2メジャー共通科目は除外

    Args:
        major1_name: 第1メジャー名（デフォルト: 'IS'）
        major2_name: 第2メジャー名（デフォルト: 'NC'）
        grade: 学年名（デフォルト: '3'）
        semester: 学期（デフォルト: '後期'）
    """
    print("=" * 80)
    print(f"課題2：SQL直接クエリ - 第1メジャー:{major1_name}, 第2メジャー:{major2_name}, {grade}年{semester}")
    print("=" * 80)

    # 学期に応じた開講区分を決定
    if semester == '前期':
        offering_categories = ['1Q', '2Q', '前期']
    elif semester == '後期':
        offering_categories = ['3Q', '4Q', '後期']
    else:  # 通年
        offering_categories = ['通年']

    # SQLiteのIN句用にプレースホルダーを動的に生成
    placeholders = ', '.join([f':cat{i}' for i in range(len(offering_categories))])

    sql = text(f"""
        SELECT DISTINCT
            c.course_title AS 科目名,
            d.day_name AS 曜日名,
            cs.period AS 時限,
            main_inst.instructor_name AS 主担当教員,
            cc.course_category_name AS 履修区分
        FROM course c
        INNER JOIN course_schedule cs ON c.timetable_code = cs.timetable_code
        INNER JOIN day_master d ON cs.day_id = d.day_id
        INNER JOIN instructor_master main_inst ON c.main_instructor_id = main_inst.instructor_id
        INNER JOIN affiliated_major am ON c.timetable_code = am.timetable_code
        INNER JOIN major_master mm ON am.major_id = mm.major_id
        LEFT JOIN course_category_master cc ON am.course_category_id = cc.course_category_id
        INNER JOIN offering_category_master oc ON c.offering_category_id = oc.offering_category_id
        WHERE mm.major_name = :major2_name
        AND oc.offering_category_name IN ({placeholders})
        AND c.timetable_code IN (
            SELECT gy2.timetable_code
            FROM grade_year gy2
            WHERE gy2.timetable_code = c.timetable_code
            GROUP BY gy2.timetable_code
            HAVING MIN(gy2.grade_name) = :grade
        )
        AND c.timetable_code NOT IN (
            SELECT am2.timetable_code
            FROM affiliated_major am2
            INNER JOIN major_master mm2 ON am2.major_id = mm2.major_id
            WHERE mm2.major_name = :major1_name
        )
        ORDER BY d.day_id, cs.period, c.course_title
    """)

    # パラメータを構築
    params = {
        'major1_name': major1_name,
        'major2_name': major2_name,
        'grade': grade,
    }
    for i, cat in enumerate(offering_categories):
        params[f'cat{i}'] = cat

    with app.app_context():
        result = db.session.execute(sql, params)

        # ファイル名の生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{OUTPUT_DIR}/query2_sql_{major1_name}_{major2_name}_{grade}_{semester}_{timestamp}.md"

        # 結果をリストに変換
        rows = list(result)

        # コンソールとファイルの両方に出力
        output_lines = []
        output_lines.append(f"\n## 検索条件")
        output_lines.append(f"- 第2メジャー: {major2_name}")
        output_lines.append(f"- 学年: {grade}")
        output_lines.append(f"- 学期: {semester}")
        output_lines.append(f"- 除外: 第1メジャー({major1_name})との共通科目")
        output_lines.append("")

        # マークダウンテーブルのヘッダー
        output_lines.append("| 科目名 | 曜日 | 時限 | 主担当教員 | 履修区分 |")
        output_lines.append("|--------|------|------|------------|----------|")

        # データ行
        for row in rows:
            course_category = row.履修区分 or '(未設定)'
            line = f"| {row.科目名} | {row.曜日名} | {row.時限} | {row.主担当教員} | {course_category} |"
            output_lines.append(line)

        output_lines.append("")
        output_lines.append(f"**合計: {len(rows)}件**")
        output_lines.append("")

        # コンソールに出力
        for line in output_lines:
            print(line)

        # ファイルに保存
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))

        print(f"結果を保存しました: {filename}\n")


def query2_sqlalchemy(major1_name='IS', major2_name='NC', grade='3', semester='後期'):
    """
    課題2：SQLAlchemyによるクエリ

    第2メジャー科目（科目名，曜日時限，主担当教員，必修・選択必修・選択の別）を全て出力
    第1メジャー・第2メジャー共通科目は除外

    Args:
        major1_name: 第1メジャー名（デフォルト: 'IS'）
        major2_name: 第2メジャー名（デフォルト: 'NC'）
        grade: 学年名（デフォルト: '3'）
        semester: 学期（デフォルト: '後期'）
    """
    print("=" * 80)
    print(f"課題2：SQLAlchemy - 第1メジャー:{major1_name}, 第2メジャー:{major2_name}, {grade}年{semester}")
    print("=" * 80)

    # 学期に応じた開講区分を決定
    if semester == '前期':
        offering_categories = ['1Q', '2Q', '前期']
    elif semester == '後期':
        offering_categories = ['3Q', '4Q', '後期']
    else:  # 通年
        offering_categories = ['通年']

    with app.app_context():
        from sqlalchemy import func

        # エイリアスを作成（第1メジャーの科目を除外するため）
        AffiliatedMajor2 = aliased(AffiliatedMajor)
        MajorMaster2 = aliased(MajorMaster)

        # 学年の最小値を持つ科目のサブクエリ
        min_grade_subquery = db.session.query(
            GradeYear.timetable_code
        ).group_by(
            GradeYear.timetable_code
        ).having(
            func.min(GradeYear.grade_name) == grade
        ).subquery()

        # 第1メジャーの科目を取得するサブクエリ
        major1_courses_subquery = db.session.query(
            AffiliatedMajor2.timetable_code
        ).join(
            MajorMaster2, AffiliatedMajor2.major_id == MajorMaster2.major_id
        ).filter(
            MajorMaster2.major_name == major1_name
        ).subquery()

        # メインクエリ
        query = db.session.query(
            Course.course_title,
            DayMaster.day_name,
            CourseSchedule.period,
            InstructorMaster.instructor_name.label('main_instructor'),
            CourseCategoryMaster.course_category_name
        ).join(
            CourseSchedule, Course.timetable_code == CourseSchedule.timetable_code
        ).join(
            DayMaster, CourseSchedule.day_id == DayMaster.day_id
        ).join(
            InstructorMaster, Course.main_instructor_id == InstructorMaster.instructor_id
        ).join(
            AffiliatedMajor, Course.timetable_code == AffiliatedMajor.timetable_code
        ).join(
            MajorMaster, AffiliatedMajor.major_id == MajorMaster.major_id
        ).outerjoin(
            CourseCategoryMaster, AffiliatedMajor.course_category_id == CourseCategoryMaster.course_category_id
        ).join(
            OfferingCategoryMaster, Course.offering_category_id == OfferingCategoryMaster.offering_category_id
        ).filter(
            MajorMaster.major_name == major2_name,
            Course.timetable_code.in_(min_grade_subquery),
            OfferingCategoryMaster.offering_category_name.in_(offering_categories),
            ~Course.timetable_code.in_(major1_courses_subquery)
        ).order_by(
            DayMaster.day_id,
            CourseSchedule.period,
            Course.course_title
        ).distinct()

        results = query.all()

        # ファイル名の生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{OUTPUT_DIR}/query2_sqlalchemy_{major1_name}_{major2_name}_{grade}_{semester}_{timestamp}.md"

        # コンソールとファイルの両方に出力
        output_lines = []
        output_lines.append(f"\n## 検索条件")
        output_lines.append(f"- 第2メジャー: {major2_name}")
        output_lines.append(f"- 学年: {grade}")
        output_lines.append(f"- 学期: {semester}")
        output_lines.append(f"- 除外: 第1メジャー({major1_name})との共通科目")
        output_lines.append("")

        # マークダウンテーブルのヘッダー
        output_lines.append("| 科目名 | 曜日 | 時限 | 主担当教員 | 履修区分 |")
        output_lines.append("|--------|------|------|------------|----------|")

        # データ行
        for row in results:
            course_category = row.course_category_name or '(未設定)'
            line = f"| {row.course_title} | {row.day_name} | {row.period} | {row.main_instructor} | {course_category} |"
            output_lines.append(line)

        output_lines.append("")
        output_lines.append(f"**合計: {len(results)}件**")
        output_lines.append("")

        # コンソールに出力
        for line in output_lines:
            print(line)

        # ファイルに保存
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))

        print(f"結果を保存しました: {filename}\n")


def main():
    """
    メイン処理：全てのクエリを実行
    """
    print("\n" + "=" * 80)
    print("Additional.txt 課題の解答例")
    print("=" * 80)
    print()

    # 課題1：SQL直接クエリ
    query1_sql(major_name='IS', grade='3', semester='後期')

    # 課題1：SQLAlchemy
    query1_sqlalchemy(major_name='IS', grade='3', semester='後期')

    # 課題2：SQL直接クエリ
    query2_sql(major1_name='IS', major2_name='NC', grade='3', semester='後期')

    # 課題2：SQLAlchemy
    query2_sqlalchemy(major1_name='IS', major2_name='NC', grade='3', semester='後期')

    # パラメータを変更してテスト
    print("\n" + "=" * 80)
    print("パラメータ変更テスト")
    print("=" * 80)
    print()

    # 2年前期のNC科目
    query1_sql(major_name='NC', grade='2', semester='前期')
    query1_sqlalchemy(major_name='NC', grade='2', semester='前期')

    print("\n" + "=" * 80)
    print("全てのクエリ実行完了")
    print("=" * 80)


if __name__ == '__main__':
    main()
