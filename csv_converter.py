"""
抽出したCSVデータをデータベース登録用に変換する関数群
文字列データをIDに変換する
"""
import csv
from typing import Dict, Tuple, Set


def create_reverse_mappings() -> Dict[str, Dict[str, int]]:
    """
    マスタデータの逆引き辞書を作成
    文字列 → ID のマッピング

    Returns:
        各マスタの逆引き辞書
    """
    # 開講区分マスタの逆引き
    offering_category_map = {
        "通年": 0,
        "1Q": 1,
        "2Q": 2,
        "3Q": 3,
        "4Q": 4,
        "前期": 5,
        "後期": 6,
    }

    # 授業形態マスタの逆引き
    class_format_map = {
        "講義": 1,
        "演習": 2,
        "実験": 3,
        "講義・演習": 4,
    }

    # 授業種別マスタの逆引き
    course_type_map = {
        "普通": 1,
        "集中": 2,
        "実験・実習": 3,
    }

    # メジャーマスタの逆引き
    major_map = {
        "IS": 1,
        "NC": 2,
        "XD": 3,
        "その他": 4,
        "情報応用科目": 5,
    }

    # 履修区分マスタの逆引き
    course_category_map = {
        "必修": 1,
        "選択必修": 2,
        "選択": 3,
        "必履修": 4,
    }

    # 曜日マスタの逆引き
    day_map = {
        "他": 0,
        "月": 1,
        "火": 2,
        "水": 3,
        "木": 4,
        "金": 5,
        "土": 6,
    }

    return {
        "offering_category": offering_category_map,
        "class_format": class_format_map,
        "course_type": course_type_map,
        "major": major_map,
        "course_category": course_category_map,
        "day": day_map,
    }


def load_master_csv(csv_path: str, id_col: str, name_col: str) -> Dict[str, int]:
    """
    マスタCSVファイルから名前→IDのマッピングを読み込む

    Args:
        csv_path: マスタCSVファイルのパス
        id_col: ID列の名前
        name_col: 名前列の名前

    Returns:
        名前→IDの辞書
    """
    mapping = {}
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping[row[name_col].strip()] = int(row[id_col])
    return mapping


def convert_courses(input_csv: str, output_csv: str,
                   instructor_map: Dict[str, int],
                   mappings: Dict[str, Dict[str, int]]) -> None:
    """
    科目CSVを変換（文字列→ID）

    Args:
        input_csv: 入力CSVファイルパス（course.csv）
        output_csv: 出力CSVファイルパス
        instructor_map: 教員名→IDのマッピング
        mappings: マスタの逆引き辞書
    """
    converted_records = []

    with open(input_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['時間割コード'].strip()
            syllabus_url = row['シラバスURL'].strip()
            course_title = row['開講科目名'].strip()
            credits = int(row['単位数'])

            # 文字列をIDに変換
            offering_category_id = mappings['offering_category'].get(row['開講区分ID'].strip())
            class_format_id = mappings['class_format'].get(row['授業形態ID'].strip())
            course_type_id = mappings['course_type'].get(row['授業種別ID'].strip())
            instructor_id = instructor_map.get(row['主担当教員ID'].strip())

            converted_records.append({
                'timetable_code': timetable_code,
                'syllabus_url': syllabus_url,
                'course_title': course_title,
                'credits': credits,
                'offering_category_id': offering_category_id,
                'class_format_id': class_format_id,
                'course_type_id': course_type_id,
                'main_instructor_id': instructor_id,
            })

    # CSV出力
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'timetable_code', 'syllabus_url', 'course_title', 'credits',
            'offering_category_id', 'class_format_id', 'course_type_id',
            'main_instructor_id'
        ])
        writer.writeheader()
        writer.writerows(converted_records)

    print(f"科目データを変換しました: {len(converted_records)}件 → {output_csv}")


def convert_course_schedules(input_csv: str, output_csv: str,
                             mappings: Dict[str, Dict[str, int]]) -> None:
    """
    開講曜限CSVを変換（文字列→ID）

    Args:
        input_csv: 入力CSVファイルパス（course_schedule.csv）
        output_csv: 出力CSVファイルパス
        mappings: マスタの逆引き辞書
    """
    converted_records = []

    with open(input_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['時間割コード'].strip()
            day_str = row['曜日'].strip()
            period_str = row['時限'].strip()

            # 「その他」の場合はスキップ（集中講義など、時間割表に表示しない）
            if day_str == 'その他' or period_str == 'その他':
                continue

            period = int(period_str)

            # 曜日を曜日IDに変換
            day_id = mappings['day'].get(day_str)

            converted_records.append({
                'timetable_code': timetable_code,
                'day_id': day_id,
                'period': period,
            })

    # CSV出力
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'timetable_code', 'day_id', 'period'
        ])
        writer.writeheader()
        writer.writerows(converted_records)

    print(f"開講曜限データを変換しました: {len(converted_records)}件 → {output_csv}")


def convert_affiliated_majors(input_csv: str, output_csv: str,
                              mappings: Dict[str, Dict[str, int]]) -> None:
    """
    所属メジャーCSVを変換（文字列→ID）

    Args:
        input_csv: 入力CSVファイルパス（affiliated_major.csv）
        output_csv: 出力CSVファイルパス
        mappings: マスタの逆引き辞書
    """
    converted_records = []

    with open(input_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['時間割コード'].strip()
            major_str = row['メジャー'].strip()
            course_category_str = row['履修区分ID'].strip()

            # 文字列をIDに変換
            major_id = mappings['major'].get(major_str)
            course_category_id = mappings['course_category'].get(course_category_str)

            converted_records.append({
                'timetable_code': timetable_code,
                'major_id': major_id,
                'course_category_id': course_category_id,
            })

    # CSV出力
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'timetable_code', 'major_id', 'course_category_id'
        ])
        writer.writeheader()
        writer.writerows(converted_records)

    print(f"所属メジャーデータを変換しました: {len(converted_records)}件 → {output_csv}")


def convert_course_classrooms(input_csv: str, output_csv: str,
                              classroom_map: Dict[str, int]) -> None:
    """
    科目教室CSVを変換（文字列→ID）

    Args:
        input_csv: 入力CSVファイルパス（course_classroom.csv）
        output_csv: 出力CSVファイルパス
        classroom_map: 教室名→IDのマッピング
    """
    converted_records = []

    with open(input_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            timetable_code = row['時間割コード'].strip()
            classroom_name = row['教室名'].strip()

            # 教室名をIDに変換
            classroom_id = classroom_map.get(classroom_name)

            converted_records.append({
                'timetable_code': timetable_code,
                'classroom_id': classroom_id,
            })

    # CSV出力
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'timetable_code', 'classroom_id'
        ])
        writer.writeheader()
        writer.writerows(converted_records)

    print(f"科目教室データを変換しました: {len(converted_records)}件 → {output_csv}")


if __name__ == '__main__':
    """
    実行例：
    python src/csv_converter.py
    """
    import os

    # ディレクトリ設定
    extracted_dir = 'docs/extracted'
    converted_dir = 'docs/converted'
    os.makedirs(converted_dir, exist_ok=True)

    print("=" * 60)
    print("CSV変換処理を開始します")
    print("=" * 60)

    # 逆引き辞書を作成
    mappings = create_reverse_mappings()

    # マスタCSVから名前→IDマッピングを読み込み
    instructor_map = load_master_csv(
        f'{extracted_dir}/instructor_master.csv',
        '教員ID',
        '教員名'
    )

    classroom_map = load_master_csv(
        f'{extracted_dir}/classroom_master.csv',
        '教室ID',
        '教室名'
    )

    # 各テーブルを変換
    convert_courses(
        f'{extracted_dir}/course.csv',
        f'{converted_dir}/course.csv',
        instructor_map,
        mappings
    )

    convert_course_schedules(
        f'{extracted_dir}/course_schedule.csv',
        f'{converted_dir}/course_schedule.csv',
        mappings
    )

    convert_affiliated_majors(
        f'{extracted_dir}/affiliated_major.csv',
        f'{converted_dir}/affiliated_major.csv',
        mappings
    )

    convert_course_classrooms(
        f'{extracted_dir}/course_classroom.csv',
        f'{converted_dir}/course_classroom.csv',
        classroom_map
    )

    # 学年データはそのままコピー（既にID形式）
    import shutil
    shutil.copy(
        f'{extracted_dir}/grade_year.csv',
        f'{converted_dir}/grade_year.csv'
    )
    print(f"学年データをコピーしました: {converted_dir}/grade_year.csv")

    # マスタデータもコピー
    shutil.copy(
        f'{extracted_dir}/instructor_master.csv',
        f'{converted_dir}/instructor_master.csv'
    )
    shutil.copy(
        f'{extracted_dir}/classroom_master.csv',
        f'{converted_dir}/classroom_master.csv'
    )
    print(f"マスタデータをコピーしました")

    print("=" * 60)
    print("すべての変換処理が完了しました")
    print("=" * 60)