"""
CSVインポート機能の使用例

DB2-1.csvファイルをデータベースにインポートする例を示します。
"""

from src import db, create_app
from src.csv_importer import import_csv_to_db, CSVImporter


def example_basic_import():
    """基本的なインポートの例"""
    app = create_app()

    with app.app_context():
        # CSVファイルをインポート
        csv_path = 'docs/DB2-1.csv'
        count = import_csv_to_db(db.session, csv_path)

        # コミット
        db.session.commit()

        print(f"✓ {count}件の科目をインポートしました")


def example_with_verification():
    """インポート後に検証を行う例"""
    app = create_app()

    with app.app_context():
        from src.models import Course, CourseOfferingHistory, GradeYear, AffiliatedMajor

        csv_path = 'docs/DB2-1.csv'

        # インポート前のレコード数
        before_count = db.session.query(Course).count()

        # インポート実行
        count = import_csv_to_db(db.session, csv_path)
        db.session.commit()

        # インポート後のレコード数
        after_count = db.session.query(Course).count()

        print(f"✓ インポート完了: {count}件")
        print(f"  - インポート前: {before_count}件")
        print(f"  - インポート後: {after_count}件")
        print(f"  - 新規追加: {after_count - before_count}件")

        # 最初の科目の詳細を表示
        first_course = db.session.query(Course).first()
        if first_course:
            print(f"\n最初の科目:")
            print(f"  時間割コード: {first_course.timetable_code}")
            print(f"  科目名: {first_course.course_title}")
            print(f"  単位数: {first_course.credits}")

            # 開講履歴
            histories = db.session.query(CourseOfferingHistory).filter_by(
                timetable_code=first_course.timetable_code
            ).all()
            if histories:
                print(f"  開講:")
                for h in histories:
                    print(f"    - {h.day.day_name}曜日 {h.period}限")

            # 学年
            grades = db.session.query(GradeYear).filter_by(
                timetable_code=first_course.timetable_code
            ).all()
            if grades:
                print(f"  対象学年: {', '.join([g.grade_name for g in grades])}年")

            # メジャー
            majors = db.session.query(AffiliatedMajor).filter_by(
                timetable_code=first_course.timetable_code
            ).all()
            if majors:
                major_names = [m.major.major_name for m in majors]
                print(f"  所属メジャー: {', '.join(major_names)}")


def example_custom_parsing():
    """カスタム処理を加えたインポートの例"""
    app = create_app()

    with app.app_context():
        importer = CSVImporter(db.session)

        # CSVを読み込み
        rows = importer.load_csv('docs/DB2-1.csv')

        print(f"CSV読み込み: {len(rows)}行")

        # 各行を処理
        imported_courses = []
        for i, row in enumerate(rows, 1):
            # カスタム処理（例: 特定のメジャーのみをインポート）
            major_str = row.get('メジャー', '')
            if 'IS' in major_str:  # ISメジャーを含む科目のみ
                course = importer.import_course_from_row(row)
                imported_courses.append(course)
                print(f"  [{i}] {course.course_title} をインポート")

        db.session.commit()
        print(f"\n✓ {len(imported_courses)}件の科目をインポートしました（IS関連のみ）")


def example_error_handling():
    """エラーハンドリングを含むインポートの例"""
    app = create_app()

    with app.app_context():
        csv_path = 'docs/DB2-1.csv'

        try:
            count = import_csv_to_db(db.session, csv_path)
            db.session.commit()
            print(f"✓ {count}件の科目をインポートしました")

        except FileNotFoundError:
            print(f"エラー: CSVファイルが見つかりません: {csv_path}")

        except Exception as e:
            print(f"エラー: インポート中に問題が発生しました: {e}")
            db.session.rollback()
            raise


def example_query_after_import():
    """インポート後にクエリを実行する例"""
    app = create_app()

    with app.app_context():
        from src.models import Course, MajorMaster, AffiliatedMajor, DayMaster, CourseOfferingHistory

        # インポート実行
        csv_path = 'docs/DB2-1.csv'
        count = import_csv_to_db(db.session, csv_path)
        db.session.commit()

        print(f"✓ {count}件の科目をインポートしました\n")

        # 1. ISメジャーの科目を検索
        print("=== ISメジャーの科目 ===")
        is_courses = db.session.query(Course)\
            .join(AffiliatedMajor, Course.timetable_code == AffiliatedMajor.timetable_code)\
            .join(MajorMaster, AffiliatedMajor.major_id == MajorMaster.major_id)\
            .filter(MajorMaster.major_name == 'IS')\
            .all()

        for course in is_courses[:5]:  # 最初の5件を表示
            print(f"  - {course.course_title} ({course.timetable_code})")

        # 2. 月曜日の科目を検索
        print("\n=== 月曜日の科目 ===")
        monday_courses = db.session.query(Course)\
            .join(CourseOfferingHistory, Course.timetable_code == CourseOfferingHistory.timetable_code)\
            .join(DayMaster, CourseOfferingHistory.day_id == DayMaster.day_id)\
            .filter(DayMaster.day_name == '月')\
            .all()

        for course in monday_courses[:5]:
            print(f"  - {course.course_title}")

        # 3. 必修科目を検索
        print("\n=== 必修科目 ===")
        required_courses = db.session.query(Course)\
            .join(Course.course_category)\
            .filter_by(course_category_name='必修')\
            .all()

        for course in required_courses[:5]:
            print(f"  - {course.course_title} ({course.credits}単位)")


if __name__ == '__main__':
    # 基本的なインポートを実行
    # example_basic_import()

    # 検証付きインポートを実行
    example_with_verification()

    # カスタム処理の例
    # example_custom_parsing()

    # エラーハンドリングの例
    # example_error_handling()

    # インポート後のクエリ例
    # example_query_after_import()
