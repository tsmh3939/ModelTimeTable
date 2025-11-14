
"""
リレーションシップを利用したデータ取得の例
Example of Using Relationships to Query Data
"""

from app import app
from src import db
from src.models import (
    Course,
    CourseSchedule,
    GradeYear,
    AffiliatedMajor,
    InstructorMaster,
    ClassroomMaster,
    MajorMaster,
    CourseCategoryMaster,
)
from src.translations.field_values import get_day_name, get_major_name


def print_separator():
    """セパレータを表示"""
    print("=" * 80)


def example1_course_schedule():
    """
    例1: 科目の開講曜限を表示
    リレーション: Course → CourseSchedule → DayMaster
    """
    print_separator()
    print("例1: 科目の開講曜限を表示")
    print_separator()

    # 科目を検索（例: 情報応用１A）
    course = Course.query.filter_by(timetable_code='S1300520_S1').first()

    if course:
        print(f"\n科目名: {course.course_title}")
        print(f"時間割コード: {course.timetable_code}")
        print(f"\n開講曜限:")

        # リレーションを使って開講曜限を取得
        for schedule in course.schedules:
            # 曜日IDから曜日名を取得
            day_name = get_day_name(schedule.day_id)
            print(f"  - {day_name}曜 {schedule.period}限")


def example2_course_with_instructor():
    """
    例2: 科目と担当教員を表示
    リレーション: Course → InstructorMaster
    """
    print_separator()
    print("例2: 科目と担当教員を表示")
    print_separator()

    # 複数の科目を取得
    courses = Course.query.limit(5).all()

    for course in courses:
        print(f"\n科目: {course.course_title}")
        print(f"  時間割コード: {course.timetable_code}")

        # リレーションを使って主担当教員を取得
        if course.main_instructor:
            print(f"  主担当教員: {course.main_instructor.instructor_name}")
        else:
            print(f"  主担当教員: 未設定")


def example3_course_with_majors():
    """
    例3: 科目の所属メジャーと履修区分を表示
    リレーション: Course → AffiliatedMajor → MajorMaster, CourseCategoryMaster
    """
    print_separator()
    print("例3: 科目の所属メジャーと履修区分を表示")
    print_separator()

    # 科目を検索（例: データ構造とアルゴリズム）
    course = Course.query.filter_by(timetable_code='S1405850_S1').first()

    if course:
        print(f"\n科目名: {course.course_title}")
        print(f"時間割コード: {course.timetable_code}")
        print(f"\n所属メジャーと履修区分:")

        # リレーションを使って所属メジャーを取得
        for affiliated in course.affiliated_majors:
            # メジャー情報を取得
            major_name = affiliated.major.major_name if affiliated.major else "不明"

            # 履修区分情報を取得
            if affiliated.course_category:
                category_name = affiliated.course_category.course_category_name
            else:
                category_name = "未設定"

            print(f"  - {major_name}: {category_name}")


def example4_course_with_classrooms():
    """
    例4: 科目の使用教室を表示
    リレーション: Course → CourseClassroom → ClassroomMaster
    """
    print_separator()
    print("例4: 科目の使用教室を表示")
    print_separator()

    # 科目を検索（例: 情報応用１A）
    course = Course.query.filter_by(timetable_code='S1300520_S1').first()

    if course:
        print(f"\n科目名: {course.course_title}")
        print(f"時間割コード: {course.timetable_code}")
        print(f"\n使用教室:")

        # リレーションを使って教室を取得
        if course.course_classrooms:
            for course_classroom in course.course_classrooms:
                classroom_name = course_classroom.classroom.classroom_name
                print(f"  - {classroom_name}")
        else:
            print("  教室情報なし")


def example5_course_with_grades():
    """
    例5: 科目の対象学年を表示
    リレーション: Course → GradeYear
    """
    print_separator()
    print("例5: 科目の対象学年を表示")
    print_separator()

    # 科目を検索（例: HCI基礎）
    course = Course.query.filter_by(timetable_code='S1408230_S1').first()

    if course:
        print(f"\n科目名: {course.course_title}")
        print(f"時間割コード: {course.timetable_code}")
        print(f"\n対象学年:")

        # リレーションを使って学年を取得
        if course.grade_years:
            grades = sorted([grade.grade_name for grade in course.grade_years])
            print(f"  {', '.join(grades)}年生")
        else:
            print("  学年情報なし")


def example6_comprehensive_course_info():
    """
    例6: 科目の詳細情報をすべて表示（総合例）
    複数のリレーションを組み合わせて使用
    """
    print_separator()
    print("例6: 科目の詳細情報（総合例）")
    print_separator()

    # 科目を検索
    course = Course.query.filter_by(timetable_code='S1407610_S1').first()

    if course:
        print(f"\n【科目情報】")
        print(f"科目名: {course.course_title}")
        print(f"時間割コード: {course.timetable_code}")
        print(f"単位数: {course.credits}単位")
        print(f"シラバスURL: {course.syllabus_url or '未設定'}")

        # 主担当教員
        print(f"\n【担当教員】")
        if course.main_instructor:
            print(f"主担当: {course.main_instructor.instructor_name}")

        # 開講曜限
        print(f"\n【開講曜限】")
        if course.schedules:
            for schedule in course.schedules:
                day_name = get_day_name(schedule.day_id)
                print(f"  {day_name}曜 {schedule.period}限")

        # 対象学年
        print(f"\n【対象学年】")
        if course.grade_years:
            grades = sorted([grade.grade_name for grade in course.grade_years])
            print(f"  {', '.join(grades)}年生")

        # 所属メジャーと履修区分
        print(f"\n【所属メジャー・履修区分】")
        if course.affiliated_majors:
            for affiliated in course.affiliated_majors:
                major_name = affiliated.major.major_name if affiliated.major else "不明"
                category_name = affiliated.course_category.course_category_name if affiliated.course_category else "未設定"
                print(f"  {major_name}: {category_name}")

        # 使用教室
        print(f"\n【使用教室】")
        if course.course_classrooms:
            classrooms = [cc.classroom.classroom_name for cc in course.course_classrooms]
            print(f"  {', '.join(classrooms)}")


def example7_reverse_relationship():
    """
    例7: 逆方向のリレーション（教員から担当科目を取得）
    リレーション: InstructorMaster → Course
    """
    print_separator()
    print("例7: 教員から担当科目を取得（逆方向リレーション）")
    print_separator()

    # 教員を検索（例: 吉廣　卓哉）
    instructor = InstructorMaster.query.filter_by(instructor_name='吉廣　卓哉').first()

    if instructor:
        print(f"\n教員名: {instructor.instructor_name}")
        print(f"\n担当科目:")

        # リレーションを使って担当科目を取得
        if instructor.main_courses:
            for course in instructor.main_courses:
                print(f"  - {course.course_title} ({course.timetable_code})")
        else:
            print("  担当科目なし")


def example8_join_query():
    """
    例8: JOINを使った検索（特定のメジャーの必修科目を取得）
    """
    print_separator()
    print("例8: 特定のメジャーの必修科目を検索")
    print_separator()

    # ISメジャーの必修科目を検索
    major = MajorMaster.query.filter_by(major_name='IS').first()
    category = CourseCategoryMaster.query.filter_by(course_category_name='必修').first()

    if major and category:
        print(f"\nメジャー: {major.major_name}")
        print(f"履修区分: {category.course_category_name}")
        print(f"\n該当科目:")

        # JOINして検索
        courses = db.session.query(Course).join(
            AffiliatedMajor
        ).filter(
            AffiliatedMajor.major_id == major.major_id,
            AffiliatedMajor.course_category_id == category.course_category_id
        ).all()

        for course in courses:
            print(f"  - {course.course_title} ({course.timetable_code})")


def main():
    """メイン処理"""
    with app.app_context():
        print("\n")
        print("=" * 80)
        print("リレーションシップを利用したデータ取得の例")
        print("=" * 80)

        try:
            # 各例を実行
            example1_course_schedule()
            example2_course_with_instructor()
            example3_course_with_majors()
            example4_course_with_classrooms()
            example5_course_with_grades()
            example6_comprehensive_course_info()
            example7_reverse_relationship()
            example8_join_query()

            print("\n")
            print_separator()
            print("すべての例の実行が完了しました")
            print_separator()
            print("\n")

        except Exception as e:
            print(f"\nエラーが発生しました: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    main()