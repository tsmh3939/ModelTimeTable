# -*- coding: utf-8 -*-
"""
メインルート
Main Routes
"""
from flask import render_template, request, redirect, url_for
from src import app
import os
from pathlib import Path

# 単位計算に必要なEnumをインポート（トップレベルのインポートに追加）
from src.translations.field_values import CourseCategoryEnum


def export_timetable_to_markdown(semester, major1_id, major2_id, timetable,
                                  semester_name, major1_name, major2_name, fiscal_year, lang='ja'):
    """
    時間割データをMarkdownファイルとして出力する関数

    Args:
        semester: セメスタID
        major1_id: 第一メジャーID
        major2_id: 第二メジャーID
        timetable: 時間割データ（辞書形式）
        semester_name: セメスタ名
        major1_name: 第一メジャー名
        major2_name: 第二メジャー名
        fiscal_year: 年度
        lang: 言語 ('ja' or 'en')

    Returns:
        str: 出力されたファイルパス
    """
    from src.translations.field_values import DAY_MASTER

    # ファイル名を生成
    filename = f"timetable_sem{semester}_major1-{major1_id}_major2-{major2_id}_{lang}.md"

    # docsディレクトリのパスを取得
    base_dir = Path(__file__).resolve().parent.parent.parent
    docs_dir = base_dir / "docs"/ "timetables"
    docs_dir.mkdir(exist_ok=True)

    filepath = docs_dir / filename

    # Markdown内容を生成
    content = []

    # ヘッダー
    content.append(f"# {fiscal_year} {semester_name}")
    content.append(f"{major1_name} × {major2_name}\n")

    # テーブルヘッダー
    header = "| 曜日 | 時限 | 科目 |"
    separator = "|------|------|------|"
    content.append(header)
    content.append(separator)

    # 各曜日・時限の行を作成
    for day_id in range(1, 6):
        day_name = DAY_MASTER[day_id][lang]
        for period in range(1, 6):
            courses = timetable[day_id][period]
            if courses:
                # 複数の科目がある場合はカンマで区切る
                course_names = ", ".join([course['course_title'] for course in courses])
                content.append(f"| {day_name} | {period} | {course_names} |")
            else:
                content.append(f"| {day_name} | {period} | |")

    # ファイルに書き込み
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

    return str(filepath)


def export_all_timetables():
    """
    全ての可能な組み合わせ(semester × major1 × major2)の時間割をMarkdownファイルとして出力する関数

    Returns:
        list: 出力されたファイルパスのリスト
    """
    from src.models import MajorMaster
    from src.translations.field_values import SEMESTERS, MajorEnum, get_semester_name, get_major_name
    from src.query import get_courses_by_semester_and_major

    exported_files = []

    # 「その他」と「情報応用科目」を除外したメジャーを取得
    majors = MajorMaster.query.filter(
        MajorMaster.major_id.notin_([MajorEnum.OTHERS, MajorEnum.INFO_APP])
    ).all()

    major_ids = [major.major_id for major in majors]

    # 全ての組み合わせをループ（同じメジャー同士を除く）
    # 4セメスタ × 3! (順列) = 4 × 6 = 24
    total_combinations = len(SEMESTERS) * len(major_ids) * (len(major_ids) - 1)
    current = 0

    for semester in SEMESTERS.keys():
        for major1_id in major_ids:
            for major2_id in major_ids:
                # 同じメジャー同士の組み合わせを除外
                if major1_id == major2_id:
                    continue

                current += 1
                print(f"処理中 ({current}/{total_combinations}): セメスタ={semester}, 第一メジャー={major1_id}, 第二メジャー={major2_id}")

                # 言語設定（日本語のみ）
                for lang in ['ja']:
                    # 名前を取得
                    semester_name = get_semester_name(semester, lang)
                    major1_name = get_major_name(major1_id, lang)
                    major2_name = get_major_name(major2_id, lang)

                    # 年度情報を取得
                    fiscal_year_dict = app.config.get('FISCAL_YEAR', {})
                    fiscal_year = fiscal_year_dict.get(lang, fiscal_year_dict.get('ja', ''))

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
                    timetable = {}
                    for day_id in range(1, 6):
                        timetable[day_id] = {}
                        for period in range(1, 6):
                            timetable[day_id][period] = []

                    # 集中講義・実験実習などのスケジュールがない科目を別途管理
                    intensive_courses = []

                    for course in all_courses:
                        if course.schedules:
                            has_regular_schedule = False
                            for schedule in course.schedules:
                                day_id = schedule.day_id
                                period = schedule.period

                                if day_id in range(1, 6) and period >= 1 and period <= 5:
                                    has_regular_schedule = True
                                    instructor_name = course.main_instructor.instructor_name if course.main_instructor else ''

                                    if course in major1_courses:
                                        major_type = 'major1'
                                    elif course in major2_courses:
                                        major_type = 'major2'
                                    elif course in others_courses:
                                        major_type = 'others'
                                    elif course in info_app_courses:
                                        major_type = 'info_app'
                                    else:
                                        major_type = 'others'

                                    already_exists = any(
                                        item['course_title'] == course.course_title
                                        for item in timetable[day_id][period]
                                    )

                                    if not already_exists:
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

                            if not has_regular_schedule:
                                instructor_name = course.main_instructor.instructor_name if course.main_instructor else ''

                                if course in major1_courses:
                                    major_type = 'major1'
                                elif course in major2_courses:
                                    major_type = 'major2'
                                elif course in others_courses:
                                    major_type = 'others'
                                elif course in info_app_courses:
                                    major_type = 'info_app'
                                else:
                                    major_type = 'others'

                                classroom_names = ', '.join([
                                    cc.classroom.classroom_name
                                    for cc in course.course_classrooms
                                ]) if course.course_classrooms else ''

                                intensive_courses.append({
                                    'course_title': course.course_title,
                                    'instructor_name': instructor_name,
                                    'major_type': major_type,
                                    'offering_category_id': course.offering_category_id,
                                    'credits': course.credits,
                                    'classroom_name': classroom_names,
                                    'syllabus_url': course.syllabus_url or '',
                                    'class_format_name': course.class_format.class_format_name if course.class_format else '',
                                    'course_type_name': course.course_type.course_type_name if course.course_type else ''
                                })
                        else:
                            instructor_name = course.main_instructor.instructor_name if course.main_instructor else ''

                            if course in major1_courses:
                                major_type = 'major1'
                            elif course in major2_courses:
                                major_type = 'major2'
                            elif course in others_courses:
                                major_type = 'others'
                            elif course in info_app_courses:
                                major_type = 'info_app'
                            else:
                                major_type = 'others'

                            classroom_names = ', '.join([
                                cc.classroom.classroom_name
                                for cc in course.course_classrooms
                            ]) if course.course_classrooms else ''

                            intensive_courses.append({
                                'course_title': course.course_title,
                                'instructor_name': instructor_name,
                                'major_type': major_type,
                                'offering_category_id': course.offering_category_id,
                                'credits': course.credits,
                                'classroom_name': classroom_names,
                                'syllabus_url': course.syllabus_url or '',
                                'class_format_name': course.class_format.class_format_name if course.class_format else '',
                                'course_type_name': course.course_type.course_type_name if course.course_type else ''
                            })

                    # 共有科目を検出
                    shared_courses = [course for course in major1_courses if course in major2_courses]

                    # 時間割の major_type を更新
                    for day_id in range(1, 6):
                        for period in range(1, 6):
                            for course_item in timetable[day_id][period]:
                                for course in shared_courses:
                                    if course.course_title == course_item['course_title']:
                                        course_item['major_type'] = 'shared'
                                        break

                    for course_item in intensive_courses:
                        for course in shared_courses:
                            if course.course_title == course_item['course_title']:
                                course_item['major_type'] = 'shared'
                                break

                    # Markdownファイルとして出力
                    filepath = export_timetable_to_markdown(
                        semester, major1_id, major2_id, timetable,
                        semester_name, major1_name, major2_name, fiscal_year, lang
                    )

                    exported_files.append(filepath)
                    print(f"  → {filepath} を出力しました")

    print(f"\n完了！合計 {len(exported_files)} ファイルを出力しました。")
    return exported_files


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


@app.route('/export-timetables')
def export_timetables_route():
    """時間割を全てMarkdownファイルとして出力するルート"""
    try:
        exported_files = export_all_timetables()
        return {
            'status': 'success',
            'message': f'合計 {len(exported_files)} ファイルを出力しました',
            'files': exported_files
        }, 200
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }, 500


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
    from src.query import get_courses_by_semester_and_major

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

    # 集中講義・実験実習などのスケジュールがない科目を別途管理
    intensive_courses = []

    for course in all_courses:
        # 各科目のスケジュールを取得
        if course.schedules:
            has_regular_schedule = False
            for schedule in course.schedules:
                day_id = schedule.day_id
                period = schedule.period

                # 月〜金のみ
                if day_id in range(1, 6):
                    # 時限が1〜5の範囲であることを確認
                    if period >= 1 and period <= 5:
                        has_regular_schedule = True
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

            # スケジュールはあるが、通常の時間割に含まれない科目
            if not has_regular_schedule:
                instructor_name = course.main_instructor.instructor_name if course.main_instructor else ''

                # どのメジャーに属するかを判定
                if course in major1_courses:
                    major_type = 'major1'
                elif course in major2_courses:
                    major_type = 'major2'
                elif course in others_courses:
                    major_type = 'others'
                elif course in info_app_courses:
                    major_type = 'info_app'
                else:
                    major_type = 'others'

                classroom_names = ', '.join([
                    cc.classroom.classroom_name
                    for cc in course.course_classrooms
                ]) if course.course_classrooms else ''

                intensive_courses.append({
                    'course_title': course.course_title,
                    'instructor_name': instructor_name,
                    'major_type': major_type,
                    'offering_category_id': course.offering_category_id,
                    'credits': course.credits,
                    'classroom_name': classroom_names,
                    'syllabus_url': course.syllabus_url or '',
                    'class_format_name': course.class_format.class_format_name if course.class_format else '',
                    'course_type_name': course.course_type.course_type_name if course.course_type else ''
                })
        else:
            # スケジュールがない科目（集中講義など）
            instructor_name = course.main_instructor.instructor_name if course.main_instructor else ''

            # どのメジャーに属するかを判定
            if course in major1_courses:
                major_type = 'major1'
            elif course in major2_courses:
                major_type = 'major2'
            elif course in others_courses:
                major_type = 'others'
            elif course in info_app_courses:
                major_type = 'info_app'
            else:
                major_type = 'others'

            classroom_names = ', '.join([
                cc.classroom.classroom_name
                for cc in course.course_classrooms
            ]) if course.course_classrooms else ''

            intensive_courses.append({
                'course_title': course.course_title,
                'instructor_name': instructor_name,
                'major_type': major_type,
                'offering_category_id': course.offering_category_id,
                'credits': course.credits,
                'classroom_name': classroom_names,
                'syllabus_url': course.syllabus_url or '',
                'class_format_name': course.class_format.class_format_name if course.class_format else '',
                'course_type_name': course.course_type.course_type_name if course.course_type else ''
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

    # 集中講義の major_type も更新
    for course_item in intensive_courses:
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
        intensive_courses=intensive_courses,
        major1_credits=major1_credits,
        shared_credits=shared_credits,
        major2_credits=major2_credits,
        others_credits=others_credits,
        info_app_credits=info_app_credits,
        total_credits=total_credits
    )
