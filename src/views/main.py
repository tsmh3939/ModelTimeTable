# -*- coding: utf-8 -*-
"""
メインルート
Main Routes
"""
from flask import render_template, request, redirect, url_for
from src import app


@app.route('/', methods=['GET', 'POST'])
def index():
    """ホームページ - 時間割選択"""
    from src.models import MajorMaster
    from src.translations.field_values import SEMESTERS, MajorEnum

    if request.method == 'POST':
        semester = request.form.get('semester', type=int)
        major1_id = request.form.get('major1_id', type=int)
        major2_id = request.form.get('major2_id', type=int)

        assert semester is not None and major1_id is not None and major2_id is not None

        # result画面にリダイレクト（クエリパラメータ付き）
        return redirect(url_for('result',
                                semester=semester,
                                major1_id=major1_id,
                                major2_id=major2_id))
    else:
        # GETリクエストの処理
        # 「その他」と「情報応用科目」を除外
        majors = MajorMaster.query.filter(
            MajorMaster.major_id.notin_([MajorEnum.OTHERS, MajorEnum.INFO_APP])
        ).all()

        return render_template(
            'index.html',
            majors=majors,
            semesters=SEMESTERS
        )


@app.route('/result')
def result():
    """時間割結果ページ"""
    from src.translations.field_values import get_semester_name, get_major_name
    from query_timetable import get_courses_by_semester_and_major

    # 現在の言語を取得（クエリパラメータから）
    current_lang = request.args.get('lang', app.config.get('DEFAULT_LANGUAGE', 'ja'))

    # 型チェック: current_langは常にstrであることを保証
    assert isinstance(current_lang, str)

    # クエリパラメータから選択内容を取得
    semester = request.args.get('semester', type=int)
    major1_id = request.args.get('major1_id', type=int)
    major2_id = request.args.get('major2_id', type=int)

    # データがない場合はホーム画面にリダイレクト
    if not all([semester, major1_id, major2_id]):
        return redirect(url_for('index'))

    # 型チェック後、semester, major1_id, major2_idはNoneではないことが保証されている
    assert semester is not None and major1_id is not None and major2_id is not None

    # 名前を取得
    semester_name = get_semester_name(semester, current_lang)
    major1_name = get_major_name(major1_id, current_lang)
    major2_name = get_major_name(major2_id, current_lang)

    # 年度情報を取得
    fiscal_year_dict = app.config.get('FISCAL_YEAR', {})
    fiscal_year = fiscal_year_dict.get(current_lang, fiscal_year_dict.get('ja', ''))

    # 第一メジャーと第二メジャーの科目を取得
    major1_courses = get_courses_by_semester_and_major(semester, major1_id)
    major2_courses = get_courses_by_semester_and_major(semester, major2_id)

    # 両メジャーの科目を統合（重複排除）
    all_courses = major1_courses.copy()
    for course in major2_courses:
        if course not in all_courses:
            all_courses.append(course)

    # 時間割を曜日・時限ごとに整理
    # timetable[day_id][period] = {'course_title': ..., 'instructor_name': ..., 'major_type': ...}
    timetable = {}
    for day_id in range(1, 6):  # 月曜(1)〜金曜(5)
        timetable[day_id] = {}

    for course in all_courses:
        # 各科目のスケジュールを取得
        if course.schedules:
            for schedule in course.schedules:
                day_id = schedule.day_id
                period = schedule.period

                # 月〜金のみ
                if day_id in range(1, 6):
                    # 時限が1〜5の範囲であることを確認
                    if period >= 1 and period <= 5:
                        # まだ授業が入っていない場合のみ追加
                        if period not in timetable[day_id]:
                            instructor_name = course.main_instructor.instructor_name if course.main_instructor else ''

                            # どのメジャーに属するかを判定（第一メジャーを優先）
                            is_in_major1 = course in major1_courses

                            if is_in_major1:
                                major_type = 'major1'  # 第一メジャー（両方に属する場合も含む）
                            else:
                                major_type = 'major2'  # 第二メジャーのみ

                            timetable[day_id][period] = {
                                'course_title': course.course_title,
                                'instructor_name': instructor_name,
                                'major_type': major_type
                            }

    # 単位数を計算
    from src.translations.field_values import CourseCategoryEnum

    # 第一メジャーの単位数を計算
    major1_credits = {'required': 0, 'elective': 0}
    for course in major1_courses:
        # このメジャーにおける履修区分を取得
        for affiliated in course.affiliated_majors:
            if affiliated.major_id == major1_id:
                category_id = affiliated.course_category_id
                credits = course.credits
                # 必修または必履修
                if category_id in [CourseCategoryEnum.REQUIRED, CourseCategoryEnum.MANDATORY]:
                    major1_credits['required'] += credits
                # 選択または選択必修
                elif category_id in [CourseCategoryEnum.ELECTIVE, CourseCategoryEnum.REQUIRED_ELECTIVE]:
                    major1_credits['elective'] += credits
                break

    # 第二メジャーの単位数を計算
    major2_credits = {'required': 0, 'elective': 0}
    for course in major2_courses:
        # このメジャーにおける履修区分を取得
        for affiliated in course.affiliated_majors:
            if affiliated.major_id == major2_id:
                category_id = affiliated.course_category_id
                credits = course.credits
                # 必修または必履修
                if category_id in [CourseCategoryEnum.REQUIRED, CourseCategoryEnum.MANDATORY]:
                    major2_credits['required'] += credits
                # 選択または選択必修
                elif category_id in [CourseCategoryEnum.ELECTIVE, CourseCategoryEnum.REQUIRED_ELECTIVE]:
                    major2_credits['elective'] += credits
                break

    # 合計単位数を計算
    total_credits = (
        major1_credits['required'] + major1_credits['elective'] +
        major2_credits['required'] + major2_credits['elective']
    )

    return render_template(
        'result.html',
        semester=semester,
        semester_name=semester_name,
        major1_id=major1_id,
        major1_name=major1_name,
        major2_id=major2_id,
        major2_name=major2_name,
        fiscal_year=fiscal_year,
        timetable=timetable,
        major1_credits=major1_credits,
        major2_credits=major2_credits,
        total_credits=total_credits
    )
