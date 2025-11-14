#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
マスタテーブルのシーディングスクリプト
Master Tables Seeding Script

このスクリプトはマスタテーブルに初期データを挿入します。
"""

import sys
from app import app
from src import db
from src.models import (
    DayMaster,
    MajorMaster,
    CourseCategoryMaster,
    OfferingCategoryMaster,
    ClassFormatMaster,
    CourseTypeMaster,
)
from src.translations.field_values import (
    DAY_MASTER,
    MAJOR_MASTER,
    COURSE_CATEGORY_MASTER,
    OFFERING_CATEGORY_MASTER,
    CLASS_FORMAT_MASTER,
    COURSE_TYPE_MASTER,
)


def seed_day_master():
    """曜日マスタをシード"""
    print("曜日マスタをシード中...")
    for day_id, names in DAY_MASTER.items():
        existing = DayMaster.query.filter_by(day_id=day_id).first()
        if not existing:
            day = DayMaster(
                day_id=day_id, # pyright: ignore[reportCallIssue]
                day_name=names['ja'] # pyright: ignore[reportCallIssue]
            )
            db.session.add(day)
            print(f"  追加: {day_id} - {names['ja']}")
        else:
            print(f"  スキップ: {day_id} - {names['ja']} (既存)")


def seed_major_master():
    """メジャーマスタをシード"""
    print("\nメジャーマスタをシード中...")
    for major_id, names in MAJOR_MASTER.items():
        existing = MajorMaster.query.filter_by(major_id=major_id).first()
        if not existing:
            major = MajorMaster(
                major_id=major_id, # pyright: ignore[reportCallIssue]
                major_name=names['ja'] # pyright: ignore[reportCallIssue]
            )
            db.session.add(major)
            print(f"  追加: {major_id} - {names['ja']}")
        else:
            print(f"  スキップ: {major_id} - {names['ja']} (既存)")


def seed_course_category_master():
    """履修区分マスタをシード"""
    print("\n履修区分マスタをシード中...")
    for cat_id, names in COURSE_CATEGORY_MASTER.items():
        existing = CourseCategoryMaster.query.filter_by(course_category_id=cat_id).first()
        if not existing:
            category = CourseCategoryMaster(
                course_category_id=cat_id, # pyright: ignore[reportCallIssue]
                course_category_name=names['ja'] # pyright: ignore[reportCallIssue]
            )
            db.session.add(category)
            print(f"  追加: {cat_id} - {names['ja']}")
        else:
            print(f"  スキップ: {cat_id} - {names['ja']} (既存)")


def seed_offering_category_master():
    """開講区分マスタをシード"""
    print("\n開講区分マスタをシード中...")
    for cat_id, names in OFFERING_CATEGORY_MASTER.items():
        existing = OfferingCategoryMaster.query.filter_by(offering_category_id=cat_id).first()
        if not existing:
            category = OfferingCategoryMaster(
                offering_category_id=cat_id, # pyright: ignore[reportCallIssue]
                offering_category_name=names['ja'] # pyright: ignore[reportCallIssue]
            )
            db.session.add(category)
            print(f"  追加: {cat_id} - {names['ja']}")
        else:
            print(f"  スキップ: {cat_id} - {names['ja']} (既存)")


def seed_class_format_master():
    """授業形態マスタをシード"""
    print("\n授業形態マスタをシード中...")
    for format_id, names in CLASS_FORMAT_MASTER.items():
        existing = ClassFormatMaster.query.filter_by(class_format_id=format_id).first()
        if not existing:
            format_obj = ClassFormatMaster(
                class_format_id=format_id, # pyright: ignore[reportCallIssue]
                class_format_name=names['ja'] # pyright: ignore[reportCallIssue]
            )
            db.session.add(format_obj)
            print(f"  追加: {format_id} - {names['ja']}")
        else:
            print(f"  スキップ: {format_id} - {names['ja']} (既存)")


def seed_course_type_master():
    """授業種別マスタをシード"""
    print("\n授業種別マスタをシード中...")
    for type_id, names in COURSE_TYPE_MASTER.items():
        existing = CourseTypeMaster.query.filter_by(course_type_id=type_id).first()
        if not existing:
            type_obj = CourseTypeMaster(
                course_type_id=type_id, # pyright: ignore[reportCallIssue]
                course_type_name=names['ja'] # pyright: ignore[reportCallIssue]
            )
            db.session.add(type_obj)
            print(f"  追加: {type_id} - {names['ja']}")
        else:
            print(f"  スキップ: {type_id} - {names['ja']} (既存)")


def seed():
    """メイン処理"""
    with app.app_context():
        print("=" * 60)
        print("マスタテーブルシーディング開始")
        print("=" * 60)

        try:
            # 各マスタテーブルをシード
            seed_day_master()
            seed_major_master()
            seed_course_category_master()
            seed_offering_category_master()
            seed_class_format_master()
            seed_course_type_master()

            # コミット
            db.session.commit()

            print("\n" + "=" * 60)
            print("✓ マスタテーブルシーディング完了")
            print("=" * 60)

            # データ確認
            print("\n【データ確認】")
            print(f"曜日マスタ: {DayMaster.query.count()}件")
            print(f"メジャーマスタ: {MajorMaster.query.count()}件")
            print(f"履修区分マスタ: {CourseCategoryMaster.query.count()}件")
            print(f"開講区分マスタ: {OfferingCategoryMaster.query.count()}件")
            print(f"授業形態マスタ: {ClassFormatMaster.query.count()}件")
            print(f"授業種別マスタ: {CourseTypeMaster.query.count()}件")

        except Exception as e:
            db.session.rollback()
            print(f"\n✗ エラーが発生しました: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    seed()