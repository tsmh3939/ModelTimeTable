"""
DB2-1.csvから各テーブル用のCSVデータを抽出する関数群
"""
import csv
from typing import List, Dict, Set, Tuple, Optional


def extract_courses(input_csv_path: str, output_csv_path: str) -> None:
    """
    科目（Course）のデータを抽出

    抽出ロジック：
    - 時間割コードをキーに重複を削除
    - 同じ時間割コードで異なるメジャーの行がある場合があるが、
      科目情報自体は同じなので最初に出現した行を使用
    - 履修区分IDは所属メジャーテーブルに属するため、ここでは抽出しない

    Args:
        input_csv_path: 入力CSVファイルのパス（DB2-1.csv）
        output_csv_path: 出力CSVファイルのパス
    """
    # 時間割コードで重複を避ける
    courses: Dict[str, Tuple[str, str, str, str, str, str, str, str]] = {}

    with open(input_csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['時間割コード'].strip()

            # 既に登録済みの時間割コードはスキップ
            if timetable_code in courses:
                continue

            syllabus_url = row['シラバスURL'].strip()
            course_title = row['開講科目名'].strip()
            credits = row['単位数'].strip()
            offering_category = row['開講区分ID'].strip()
            class_format = row['授業形態ID'].strip()
            course_type = row['授業種別ID'].strip()
            main_instructor = row['主担当教員ID'].strip()

            courses[timetable_code] = (
                timetable_code,
                syllabus_url,
                course_title,
                credits,
                offering_category,
                class_format,
                course_type,
                main_instructor
            )

    # CSVに書き出し
    with open(output_csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            '時間割コード',
            'シラバスURL',
            '開講科目名',
            '単位数',
            '開講区分ID',
            '授業形態ID',
            '授業種別ID',
            '主担当教員ID'
        ])

        # ソートして書き出し
        for timetable_code in sorted(courses.keys()):
            writer.writerow(courses[timetable_code])

    print(f"科目データを抽出しました: {len(courses)}件 → {output_csv_path}")


def extract_offering_history(input_csv_path: str, output_csv_path: str) -> None:
    """
    開講曜限（CourseSchedule）のデータを抽出

    抽出ロジック：
    - 曜日列を1文字ずつ分割（月火水木金土日）
    - 時限列を1文字ずつ分割（1-6限）
    - 曜日の数と時限の数が等しい場合：ペアで対応（例：水金,11 → 水1限,金1限）
    - 曜日が1つで時限が複数：その曜日の全時限（例：火,34 → 火3限,火4限）

    Args:
        input_csv_path: 入力CSVファイルのパス（DB2-1.csv）
        output_csv_path: 出力CSVファイルのパス
    """
    # 重複を避けるためにSetで管理
    records: Set[Tuple[str, str, str]] = set()

    with open(input_csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['時間割コード'].strip()
            days_str = row['曜日'].strip()
            periods_str = row['時限'].strip()

            # 「その他」の場合はスキップ（集中講義など、時間割表に表示しない）
            if days_str == 'その他' or periods_str == 'その他':
                continue

            # 曜日を1文字ずつ分割
            days = list(days_str)
            # 時限を1文字ずつ分割
            periods = list(periods_str)

            # 曜日と時限の組み合わせを生成
            if len(days) == len(periods):
                # 曜日と時限がペアで対応する場合（例：水金,11 → 水1限,金1限）
                for day, period in zip(days, periods):
                    records.add((timetable_code, day, period))
            elif len(days) == 1:
                # 曜日が1つで時限が複数の場合（例：火,34 → 火3限,火4限）
                for period in periods:
                    records.add((timetable_code, days[0], period))
            elif len(periods) == 1:
                # 時限が1つで曜日が複数の場合（例：月水,1 → 月1限,水1限）
                for day in days:
                    records.add((timetable_code, day, periods[0]))
            else:
                # その他の場合は全組み合わせ（念のため）
                for day in days:
                    for period in periods:
                        records.add((timetable_code, day, period))

    # CSVに書き出し
    with open(output_csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['時間割コード', '曜日', '時限'])

        # ソートして書き出し
        for record in sorted(records):
            writer.writerow(record)

    print(f"開講曜限データを抽出しました: {len(records)}件 → {output_csv_path}")


def extract_grade_years(input_csv_path: str, output_csv_path: str) -> None:
    """
    学年（GradeYear）のデータを抽出

    抽出ロジック：
    - 学年列を1文字ずつ分割
    - 各文字を学年名として出力（234 → "2","3","4"）

    Args:
        input_csv_path: 入力CSVファイルのパス（DB2-1.csv）
        output_csv_path: 出力CSVファイルのパス
    """
    # 重複を避けるためにSetで管理
    records: Set[Tuple[str, str]] = set()

    with open(input_csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['時間割コード'].strip()
            grades_str = row['学年 '].strip()  # カラム名の後ろにスペースあり

            # 学年を1文字ずつ分割
            for grade in grades_str:
                if grade.strip():  # 空白文字を除外
                    records.add((timetable_code, grade))

    # CSVに書き出し
    with open(output_csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['時間割コード', '学年名'])

        # ソートして書き出し
        for record in sorted(records):
            writer.writerow(record)

    print(f"学年データを抽出しました: {len(records)}件 → {output_csv_path}")


def extract_affiliated_majors(input_csv_path: str, output_csv_path: str) -> None:
    """
    所属メジャー（AffiliatedMajor）のデータを抽出

    抽出ロジック：
    - メジャー列を2文字ずつ分割（IS, NC, XD等）
    - "その他"のうち、開講科目名に「情報応用」が含まれる場合は「情報応用科目」として扱う
    - それ以外の"その他"は1つのメジャーとして扱う
    - 同じ時間割コードでもメジャーごとに履修区分IDが異なる場合があるため、
      元のCSVの行ごとに処理

    Args:
        input_csv_path: 入力CSVファイルのパス（DB2-1.csv）
        output_csv_path: 出力CSVファイルのパス
    """
    # 重複を避けるためにSetで管理
    records: Set[Tuple[str, str, str]] = set()

    with open(input_csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['時間割コード'].strip()
            course_title = row['開講科目名'].strip()
            majors_str = row['メジャー'].strip()
            course_category = row['履修区分ID'].strip()

            # メジャーの分割
            if majors_str == 'その他':
                # 開講科目名に「情報応用」が含まれる場合は「情報応用科目」として扱う
                if '情報応用' in course_title:
                    records.add((timetable_code, '情報応用科目', course_category))
                else:
                    # それ以外の"その他"は1つのメジャーとして扱う
                    records.add((timetable_code, majors_str, course_category))
            else:
                # 2文字ずつ分割（IS, NC, XD等）
                for i in range(0, len(majors_str), 2):
                    major = majors_str[i:i+2]
                    if major:  # 空でない場合のみ追加
                        records.add((timetable_code, major, course_category))

    # CSVに書き出し
    with open(output_csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['時間割コード', 'メジャー', '履修区分ID'])

        # ソートして書き出し
        for record in sorted(records):
            writer.writerow(record)

    print(f"所属メジャーデータを抽出しました: {len(records)}件 → {output_csv_path}")


def extract_instructors(input_csv_path: str, output_csv_path: str) -> None:
    """
    教員マスタ（InstructorMaster）のデータを抽出

    抽出ロジック：
    - 主担当教員ID列から一意の教員名を抽出
    - 自動採番でIDを割り当て（1から開始）

    Args:
        input_csv_path: 入力CSVファイルのパス（DB2-1.csv）
        output_csv_path: 出力CSVファイルのパス
    """
    # 一意の教員名を収集
    instructors: Set[str] = set()

    with open(input_csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            instructor_name = row['主担当教員ID'].strip()
            if instructor_name:  # 空でない場合のみ追加
                instructors.add(instructor_name)

    # CSVに書き出し（ソートしてからIDを割り当て）
    with open(output_csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['教員ID', '教員名'])

        # ソートして書き出し
        for idx, instructor_name in enumerate(sorted(instructors), start=1):
            writer.writerow([idx, instructor_name])

    print(f"教員マスタデータを抽出しました: {len(instructors)}件 → {output_csv_path}")


def extract_classrooms(input_csv_path: str, output_csv_path: str) -> None:
    """
    教室マスタ（ClassroomMaster）のデータを抽出

    抽出ロジック：
    - 教室名列からスペース区切りで一意の教室名を抽出
    - 自動採番でIDを割り当て（1から開始）

    Args:
        input_csv_path: 入力CSVファイルのパス（DB2-1.csv）
        output_csv_path: 出力CSVファイルのパス
    """
    # 一意の教室名を収集
    classrooms: Set[str] = set()

    with open(input_csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            classroom_names = row['教室名'].strip()
            if classroom_names:
                # スペース区切りで分割
                for classroom in classroom_names.split():
                    if classroom.strip():
                        classrooms.add(classroom.strip())

    # CSVに書き出し（ソートしてからIDを割り当て）
    with open(output_csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['教室ID', '教室名'])

        # ソートして書き出し
        for idx, classroom_name in enumerate(sorted(classrooms), start=1):
            writer.writerow([idx, classroom_name])

    print(f"教室マスタデータを抽出しました: {len(classrooms)}件 → {output_csv_path}")


def extract_course_classrooms(input_csv_path: str, output_csv_path: str) -> None:
    """
    科目教室（CourseClassroom）中間テーブルのデータを抽出

    抽出ロジック：
    - 教室名列からスペース区切りで教室を分割
    - 各科目と教室の組み合わせを出力
    - 教室名はマスタと照合する必要があるため、名前のまま出力

    Args:
        input_csv_path: 入力CSVファイルのパス（DB2-1.csv）
        output_csv_path: 出力CSVファイルのパス
    """
    # 重複を避けるためにSetで管理
    records: Set[Tuple[str, str]] = set()

    with open(input_csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['時間割コード'].strip()
            classroom_names = row['教室名'].strip()

            if classroom_names:
                # スペース区切りで分割
                for classroom in classroom_names.split():
                    if classroom.strip():
                        records.add((timetable_code, classroom.strip()))

    # CSVに書き出し
    with open(output_csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['時間割コード', '教室名'])

        # ソートして書き出し
        for record in sorted(records):
            writer.writerow(record)

    print(f"科目教室データを抽出しました: {len(records)}件 → {output_csv_path}")


if __name__ == '__main__':
    """
    実行例：
    python src/csv_extractor.py
    """
    import os

    # 入力ファイル
    input_file = 'docs/DB2-1.csv'

    # 出力ディレクトリを作成
    output_dir = 'docs/extracted'
    os.makedirs(output_dir, exist_ok=True)

    # 各関数を実行
    print("=" * 60)
    print("CSV抽出処理を開始します")
    print("=" * 60)

    extract_courses(
        input_file,
        f'{output_dir}/course.csv'
    )

    extract_offering_history(
        input_file,
        f'{output_dir}/course_schedule.csv'
    )

    extract_grade_years(
        input_file,
        f'{output_dir}/grade_year.csv'
    )

    extract_affiliated_majors(
        input_file,
        f'{output_dir}/affiliated_major.csv'
    )

    extract_instructors(
        input_file,
        f'{output_dir}/instructor_master.csv'
    )

    extract_classrooms(
        input_file,
        f'{output_dir}/classroom_master.csv'
    )

    extract_course_classrooms(
        input_file,
        f'{output_dir}/course_classroom.csv'
    )

    print("=" * 60)
    print("すべての抽出処理が完了しました")
    print("=" * 60)