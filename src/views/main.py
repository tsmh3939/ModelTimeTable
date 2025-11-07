# -*- coding: utf-8 -*-
"""
メインルート
Main Routes
"""
from flask import render_template, request, redirect, url_for
from src import app

# 単位計算に必要なEnumをインポート（トップレベルのインポートに追加）
from src.translations.field_values import CourseCategoryEnum


def calculate_credits(course_list, major_id):
    """
    指定された科目リストとメジャーIDに基づき、必修・選択単位を計算するヘルパー関数。
    """
    credits = {'required': 0, 'elective': 0}
    for course in course_list:
        # このメジャーにおける履修区分を取得
        for affiliated in course.affiliated_majors:
            if affiliated.major_id == major_id:
                category_id = affiliated.course_category_id
                credits_val = course.credits
                # 必修または必履修
                if category_id in [CourseCategoryEnum.REQUIRED, CourseCategoryEnum.MANDATORY]:
                    credits['required'] += credits_val
                # 選択または選択必修
                elif category_id in [CourseCategoryEnum.ELECTIVE, CourseCategoryEnum.REQUIRED_ELECTIVE]:
                    credits['elective'] += credits_val
                break
    return credits


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
    from src.translations.field_values import get_semester_name, get_major_name, MajorEnum
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

    # その他メジャーと情報応用科目も取得
    others_courses = get_courses_by_semester_and_major(semester, MajorEnum.OTHERS)
    info_app_courses = get_courses_by_semester_and_major(semester, MajorEnum.INFO_APP)

    # 全メジャーの科目を統合（重複排除）
    all_courses = major1_courses.copy()
    for course in major2_courses:
        if course not in all_courses:
            all_courses.append(course)
    for course in others_courses:
        if course not in all_courses:
            all_courses.append(course)
    for course in info_app_courses:
        if course not in all_courses:
            all_courses.append(course)

    # 時間割を曜日・時限ごとに整理
    # timetable[day_id][period] = [{'course_title': ..., 'instructor_name': ..., 'major_type': ...}, ...]
    timetable = {}
    for day_id in range(1, 6):  # 月曜(1)〜金曜(5)
        timetable[day_id] = {}
        for period in range(1, 6):  # 1〜5限
            timetable[day_id][period] = []  # リストで初期化

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
                        instructor_name = course.main_instructor.instructor_name if course.main_instructor else ''

                        # どのメジャーに属するかを判定（優先順位: 第一 > 第二 > その他 > 情報応用）
                        if course in major1_courses:
                            major_type = 'major1'
                        elif course in major2_courses:
                            major_type = 'major2'
                        elif course in others_courses:
                            major_type = 'others'
                        elif course in info_app_courses:
                            major_type = 'info_app'
                        else:
                            major_type = 'others'  # デフォルト

                        # 同じ科目が既に登録されていないかチェック
                        already_exists = any(
                            item['course_title'] == course.course_title
                            for item in timetable[day_id][period]
                        )

                        if not already_exists:
                            # 教室名を取得（複数ある場合はカンマ区切り）
                            classroom_names = ', '.join([
                                cc.classroom.classroom_name
                                for cc in course.course_classrooms
                            ]) if course.course_classrooms else ''

                            timetable[day_id][period].append({
                                'course_title': course.course_title,
                                'instructor_name': instructor_name,
                                'major_type': major_type,
                                'offering_category_id': course.offering_category_id,
                                'credits': course.credits,
                                'classroom_name': classroom_names,
                                'syllabus_url': course.syllabus_url or ''
                            })

    # 単位数を計算
    # 共有科目を検出（第一メジャーと第二メジャーの両方に属する科目）
    shared_courses = [course for course in major1_courses if course in major2_courses]

    # 時間割の major_type を更新：共有科目を 'shared' に変更
    for day_id in range(1, 6):
        for period in range(1, 6):
            for course_item in timetable[day_id][period]:
                # この科目が共有科目かチェック
                for course in shared_courses:
                    if course.course_title == course_item['course_title']:
                        course_item['major_type'] = 'shared'
                        break

    # --- 単位計算の関数化適用 ---

    # 第一メジャーの単位数を計算（共有科目を除く）
    major1_courses_exclusive = [course for course in major1_courses if course not in shared_courses]
    major1_credits = calculate_credits(major1_courses_exclusive, major1_id)

    # 情報学領域共有科目の単位数を計算
    # 共有科目は、第一メジャーの履修区分で計算する（元のロジックを維持）
    shared_credits = calculate_credits(shared_courses, major1_id)

    # 第二メジャーの単位数を計算（共有科目を除く）
    major2_courses_exclusive = [course for course in major2_courses if course not in shared_courses]
    major2_credits = calculate_credits(major2_courses_exclusive, major2_id)

    # その他メジャーの単位数を計算
    others_credits = calculate_credits(others_courses, MajorEnum.OTHERS)

    # 情報応用科目の単位数を計算
    info_app_credits = calculate_credits(info_app_courses, MajorEnum.INFO_APP)

    # --- 合計単位数を計算 ---
    total_credits = (
        major1_credits['required'] + major1_credits['elective'] +
        shared_credits['required'] + shared_credits['elective'] +
        major2_credits['required'] + major2_credits['elective'] +
        others_credits['required'] + others_credits['elective'] +
        info_app_credits['required'] + info_app_credits['elective']
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
        shared_credits=shared_credits,
        major2_credits=major2_credits,
        others_credits=others_credits,
        info_app_credits=info_app_credits,
        total_credits=total_credits
    )