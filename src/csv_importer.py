"""
CSVファイルからデータベースへのインポート機能

DB2-1.csv形式のCSVファイルをデータベースモデルに変換し、
適切なテーブルにレコードを挿入する機能を提供します。
"""

import csv
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from src.models import (
    Course, CourseOfferingHistory, GradeYear, AffiliatedMajor,
    CourseCategoryMaster, OfferingCategoryMaster, ClassFormatMaster,
    CourseTypeMaster, InstructorMaster, DayMaster, MajorMaster
)


class CSVImporter:
    """CSVデータをデータベースにインポートするクラス"""

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemyのセッション
        """
        self.session = session
        self._day_map = {}  # 曜日名 -> DayMasterのキャッシュ
        self._major_map = {}  # メジャー名 -> MajorMasterのキャッシュ
        self._category_map = {}  # 履修区分名 -> CourseCategoryMasterのキャッシュ
        self._offering_map = {}  # 開講区分名 -> OfferingCategoryMasterのキャッシュ
        self._format_map = {}  # 授業形態名 -> ClassFormatMasterのキャッシュ
        self._type_map = {}  # 授業種別名 -> CourseTypeMasterのキャッシュ
        self._instructor_map = {}  # 教員名 -> InstructorMasterのキャッシュ

    def load_csv(self, csv_path: str, encoding: str = 'utf-8-sig') -> List[Dict[str, str]]:
        """
        CSVファイルを読み込んで辞書のリストとして返す

        Args:
            csv_path: CSVファイルのパス
            encoding: ファイルのエンコーディング（デフォルト: utf-8-sig）

        Returns:
            各行を辞書として格納したリスト
        """
        rows = []
        with open(csv_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 空行をスキップ
                if not row.get('時間割コード'):
                    continue
                rows.append(row)
        return rows

    def get_or_create_day(self, day_name: str) -> Optional[DayMaster]:
        """
        曜日マスタを取得または作成

        Args:
            day_name: 曜日名（例: "月", "火水"）

        Returns:
            DayMasterインスタンス、または空文字列の場合はNone
        """
        if not day_name:
            return None

        if day_name not in self._day_map:
            day = self.session.query(DayMaster).filter_by(day_name=day_name).first()
            if not day:
                day = DayMaster(day_name=day_name)
                self.session.add(day)
                self.session.flush()  # IDを取得
            self._day_map[day_name] = day

        return self._day_map[day_name]

    def get_or_create_major(self, major_name: str) -> Optional[MajorMaster]:
        """
        メジャーマスタを取得または作成

        Args:
            major_name: メジャー名（例: "IS", "NC"）

        Returns:
            MajorMasterインスタンス、または空文字列の場合はNone
        """
        if not major_name:
            return None

        if major_name not in self._major_map:
            major = self.session.query(MajorMaster).filter_by(major_name=major_name).first()
            if not major:
                major = MajorMaster(major_name=major_name)
                self.session.add(major)
                self.session.flush()
            self._major_map[major_name] = major

        return self._major_map[major_name]

    def get_or_create_course_category(self, category_name: str) -> Optional[CourseCategoryMaster]:
        """履修区分マスタを取得または作成"""
        if not category_name:
            return None

        if category_name not in self._category_map:
            category = self.session.query(CourseCategoryMaster).filter_by(
                course_category_name=category_name
            ).first()
            if not category:
                category = CourseCategoryMaster(course_category_name=category_name)
                self.session.add(category)
                self.session.flush()
            self._category_map[category_name] = category

        return self._category_map[category_name]

    def get_or_create_offering_category(self, offering_name: str) -> Optional[OfferingCategoryMaster]:
        """開講区分マスタを取得または作成"""
        if not offering_name:
            return None

        if offering_name not in self._offering_map:
            offering = self.session.query(OfferingCategoryMaster).filter_by(
                offering_category_name=offering_name
            ).first()
            if not offering:
                offering = OfferingCategoryMaster(offering_category_name=offering_name)
                self.session.add(offering)
                self.session.flush()
            self._offering_map[offering_name] = offering

        return self._offering_map[offering_name]

    def get_or_create_class_format(self, format_name: str) -> Optional[ClassFormatMaster]:
        """授業形態マスタを取得または作成"""
        if not format_name:
            return None

        if format_name not in self._format_map:
            format_master = self.session.query(ClassFormatMaster).filter_by(
                class_format_name=format_name
            ).first()
            if not format_master:
                format_master = ClassFormatMaster(class_format_name=format_name)
                self.session.add(format_master)
                self.session.flush()
            self._format_map[format_name] = format_master

        return self._format_map[format_name]

    def get_or_create_course_type(self, type_name: str) -> Optional[CourseTypeMaster]:
        """授業種別マスタを取得または作成"""
        if not type_name:
            return None

        if type_name not in self._type_map:
            course_type = self.session.query(CourseTypeMaster).filter_by(
                course_type_name=type_name
            ).first()
            if not course_type:
                course_type = CourseTypeMaster(course_type_name=type_name)
                self.session.add(course_type)
                self.session.flush()
            self._type_map[type_name] = course_type

        return self._type_map[type_name]

    def get_or_create_instructor(self, instructor_name: str) -> Optional[InstructorMaster]:
        """教員マスタを取得または作成"""
        if not instructor_name:
            return None

        if instructor_name not in self._instructor_map:
            instructor = self.session.query(InstructorMaster).filter_by(
                instructor_name=instructor_name
            ).first()
            if not instructor:
                instructor = InstructorMaster(instructor_name=instructor_name)
                self.session.add(instructor)
                self.session.flush()
            self._instructor_map[instructor_name] = instructor

        return self._instructor_map[instructor_name]

    def parse_grade_years(self, grade_str: str) -> List[str]:
        """
        学年文字列をパースして学年リストに変換

        Args:
            grade_str: 学年文字列（例: "234" -> ["2", "3", "4"]）

        Returns:
            学年のリスト
        """
        if not grade_str:
            return []
        return [char for char in grade_str if char.isdigit()]

    def parse_majors(self, major_str: str) -> List[str]:
        """
        メジャー文字列をパースしてメジャーリストに変換

        Args:
            major_str: メジャー文字列（例: "ISNCXD" -> ["IS", "NC", "XD"]）

        Returns:
            メジャーのリスト
        """
        if not major_str:
            return []

        # 2文字ずつ分割（IS, NC, XD等）
        majors = []
        i = 0
        while i < len(major_str):
            if i + 1 < len(major_str):
                major = major_str[i:i+2]
                majors.append(major)
                i += 2
            else:
                # 奇数文字の場合は1文字で追加
                majors.append(major_str[i])
                i += 1

        return majors

    def parse_days_and_periods(self, day_str: str, period_str: str) -> List[Tuple[str, int]]:
        """
        曜日と時限の文字列をパースして(曜日, 時限)のリストに変換

        Args:
            day_str: 曜日文字列（例: "月", "水金"）
            period_str: 時限文字列（例: "1", "34", "11"）

        Returns:
            (曜日, 時限)のタプルのリスト
        """
        if not day_str or not period_str:
            return []

        days = list(day_str)  # "水金" -> ["水", "金"]
        periods = [int(p) for p in period_str if p.isdigit()]  # "34" -> [3, 4]

        # 曜日と時限の組み合わせを生成
        result = []
        if len(days) == 1 and len(periods) >= 1:
            # 1つの曜日に複数の時限
            for period in periods:
                result.append((days[0], period))
        elif len(days) == len(periods):
            # 複数の曜日と時限が対応
            for day, period in zip(days, periods):
                result.append((day, period))
        elif len(days) > 1 and len(periods) == 1:
            # 複数の曜日に同じ時限
            for day in days:
                result.append((day, periods[0]))
        else:
            # その他のケース（全組み合わせ）
            for day in days:
                for period in periods:
                    result.append((day, period))

        return result

    def import_course_from_row(self, row: Dict[str, str]) -> Course:
        """
        CSV行データからCourseレコードとその関連レコードを作成

        Args:
            row: CSV行データの辞書

        Returns:
            作成されたCourseインスタンス
        """
        timetable_code = row['時間割コード']

        # 既存のCourseを取得（存在しない場合は新規作成）
        course = self.session.query(Course).filter_by(timetable_code=timetable_code).first()

        if not course:
            # マスタデータの取得または作成
            category = self.get_or_create_course_category(row.get('履修区分ID', ''))
            offering = self.get_or_create_offering_category(row.get('開講区分ID', ''))
            class_format = self.get_or_create_class_format(row.get('授業形態ID', ''))
            course_type = self.get_or_create_course_type(row.get('授業種別ID', ''))
            instructor = self.get_or_create_instructor(row.get('主担当教員ID', ''))

            # Courseの作成
            course = Course(
                timetable_code=timetable_code,
                course_title=row.get('開講科目名', ''),
                credits=int(row.get('単位数', 0)) if row.get('単位数') else 0,
                course_category_id=category.course_category_id if category else None,
                offering_category_id=offering.offering_category_id if offering else None,
                class_format_id=class_format.class_format_id if class_format else None,
                course_type_id=course_type.course_type_id if course_type else None,
                main_instructor_id=instructor.instructor_id if instructor else None
            )
            self.session.add(course)
            self.session.flush()

        # 開講履歴の追加
        day_period_list = self.parse_days_and_periods(
            row.get('曜日', ''),
            row.get('時限', '')
        )

        for day_name, period in day_period_list:
            day = self.get_or_create_day(day_name)
            if day:
                # 既存の開講履歴をチェック
                existing = self.session.query(CourseOfferingHistory).filter_by(
                    timetable_code=timetable_code,
                    day_id=day.day_id
                ).first()

                if not existing:
                    history = CourseOfferingHistory(
                        timetable_code=timetable_code,
                        day_id=day.day_id,
                        period=period
                    )
                    self.session.add(history)

        # 学年の追加
        grade_years = self.parse_grade_years(row.get('学年', ''))
        for grade in grade_years:
            existing = self.session.query(GradeYear).filter_by(
                timetable_code=timetable_code,
                grade_name=grade
            ).first()

            if not existing:
                grade_year = GradeYear(
                    timetable_code=timetable_code,
                    grade_name=grade
                )
                self.session.add(grade_year)

        # 所属メジャーの追加
        majors = self.parse_majors(row.get('メジャー', ''))
        for major_name in majors:
            major = self.get_or_create_major(major_name)
            if major:
                existing = self.session.query(AffiliatedMajor).filter_by(
                    timetable_code=timetable_code,
                    major_id=major.major_id
                ).first()

                if not existing:
                    affiliated = AffiliatedMajor(
                        timetable_code=timetable_code,
                        major_id=major.major_id
                    )
                    self.session.add(affiliated)

        return course

    def import_from_csv(self, csv_path: str, encoding: str = 'utf-8-sig') -> int:
        """
        CSVファイルからデータをインポート

        Args:
            csv_path: CSVファイルのパス
            encoding: ファイルのエンコーディング

        Returns:
            インポートした科目数
        """
        rows = self.load_csv(csv_path, encoding)
        course_count = 0

        for row in rows:
            self.import_course_from_row(row)
            course_count += 1

        # コミットは呼び出し側で行う
        return course_count


def import_csv_to_db(session: Session, csv_path: str, encoding: str = 'utf-8-sig') -> int:
    """
    CSVファイルをデータベースにインポートする便利関数

    Args:
        session: SQLAlchemyセッション
        csv_path: CSVファイルのパス
        encoding: ファイルのエンコーディング

    Returns:
        インポートした科目数

    Example:
        from src import db
        from src.csv_importer import import_csv_to_db

        count = import_csv_to_db(db.session, 'docs/DB2-1.csv')
        db.session.commit()
        print(f"{count}件の科目をインポートしました")
    """
    importer = CSVImporter(session)
    count = importer.import_from_csv(csv_path, encoding)
    return count